import os
import re
import sys

import numpy as np

import logging as logger
logger.basicConfig(level=logger.WARN)

import obspy
#from obspy import read_inventory
from .stationxml_obs import _read_stationxml
from . import installation_dir

from obspy.core.inventory.response import PolesZerosResponseStage, FIRResponseStage
from obspy.core.inventory.response import ResponseStage, CoefficientsTypeResponseStage
from obspy.core.inventory.response import PolynomialResponseStage
from obspy.core.inventory.response import InstrumentPolynomial
from obspy.core.inventory.response import InstrumentSensitivity
from obspy.core.inventory.response import ResponseListResponseStage
from obspy.geodetics import gps2dist_azimuth

from .iris_rules import error_codes, restrictions, test_xmls
from .iris_unit_names import unit_names
#from iris_rules import error_codes, restrictions, test_xmls
#from iris_unit_names import unit_names
unit_names_lower = [x.lower() for x in unit_names]

class epoch():
    def __init__(self, start_date=None, end_date=None):
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f'[{self.start_date} - {self.end_date}]'

#non_traditional_orientations = "1 — Channel Azimuth is greater than 5 degrees from north (Reversed: south).\n" \
                               #"2 — Channel Azimuth is greater than 5 degrees from east (Reversed: west).\n" \
                               #"3 — Channel Dip is greater than 5 degrees from vertical."
non_traditional_orientations = ("1 -  Channel Azimuth is greater than 5 degrees from north (Reversed: south).\n"
                                "2 -  Channel Azimuth is greater than 5 degrees from east (Reversed: west).\n"
                                "3 -  Channel Dip is greater than 5 degrees from vertical.")

class stationxml_validator():
    '''
    Class to read stationxml into Inventory (if necessary) and validate inventory
    '''

    station_code = None

    def __init__(self, stationxml_or_inventory):
        #self.stationxml = stationxml
        self.errors = []
        self.warnings = []
        self.return_codes = []

        self.network_errors = []
        self.station_errors = []
        self.channel_errors = []
        self.response_errors = []

        self.inv = None

        if isinstance(stationxml_or_inventory, obspy.core.inventory.inventory.Inventory):
            self.stationxml = None
            self.inv = stationxml_or_inventory
            #print("HERE: validate against already read Inventory object")

        else:
            self.stationxml = stationxml_or_inventory
            logger.debug("stationxml_validator: attempt to read file=[%s]" % self.stationxml)
            try:
                #self.inv = read_inventory(self.stationxml, format="STATIONXML")
                self.inv = _read_stationxml(self.stationxml)
                #print(self.inv)
            except Exception as ex:
                template = "read_inventory: An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)

    def validate_inventory(self):
        if self.inv is None:
            print("Unable to validate_inventory as it wasn't read properly")
            return

        for network in self.inv.networks:
            #print("validate network")
            self.validate_network(network)
            for station in network.stations:
                #print("validate station")
                self.station_code = station.code[:]
                self.validate_station(station)
                for channel in station.channels:
                    #print("validate channel")
                    #print("validate channel=%s sr:%f" % (channel.code, channel.sample_rate))
                    self.validate_channel(channel)
                    if channel.response:
                        #print("validate response")
                        self.validate_response(channel)

    def validate_network(self, network):
        for rule_code in get_rules(level='network'):
            func_name = "self.validate_rule_%s" % rule_code
            logger.debug("call func:%s for net code:%s" % (func_name, network.code))
            eval(func_name)(network)
        return

    def validate_station(self, station):
        for rule_code in get_rules(level='station'):
            func_name = "self.validate_rule_%s" % rule_code
            logger.debug("call func:%s for stn code:%s" % (func_name, station.code))
            eval(func_name)(station)
        return

    def validate_channel(self, channel):
        for rule_code in get_rules(level='channel'):
            func_name = "self.validate_rule_%s" % rule_code
            if enforce_rule(channel, rule_code):
                logger.debug("call func:%s for chn code:%s" % (func_name, channel.code))
                eval(func_name)(channel)
            else:
                logger.debug("Rule:[%s] --> Skip Chn:%s" % (rule_code, channel.code))
        return

    def validate_response(self, channel):
        for rule_code in get_rules(level='response'):
            func_name = "self.validate_rule_%s" % rule_code
            if enforce_rule(channel, rule_code):
                logger.debug("call func:%s for chn code:%s" % (func_name, channel.code))
                eval(func_name)(channel)
            else:
                logger.debug("Rule:[%s] --> Skip Chn:%s" % (rule_code, channel.code))
        return

    def validate_rule(self, rule_code):
        func_name = "self.validate_rule_%s" % rule_code

        if rule_code not in error_codes.keys():
            logger.error("validate_rule: Unknown rule_code:%s" % rule_code)
            return

        if rule_code[0] == '1':
            for network in self.inv.networks:
                eval(func_name)(network)
        elif rule_code[0] == '2':
            for network in self.inv.networks:
                for station in network.stations:
                    eval(func_name)(station)
        elif rule_code[0] in ['3', '4']:
            for network in self.inv.networks:
                for station in network.stations:
                    for channel in station.channels:
                        eval(func_name)(channel)
        return

    # <-- Network Definition Errors -->
    # 101 Network:Code must be assigned a string consisting of 1-2 uppercase characters A-Z and or 
    #                  numeric characters 0-9.
    def validate_rule_101(self, network):
        rule_code = '101'
        #print("Inside validate_rule_101 network.code=[%s]" % network.code)
        if not valid_ascii(network.code, 1, 2):
            msg = "Invalid network code: [%s]" % network.code
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        return True 

    # <-- Network Time Errors -->
    # 110 If Network:startDate is included then it must occur before Network:endDate if 
    #   Network:endDate is included. [112]
    def validate_rule_110(self, network):
        rule_code = '110'
        if network.start_date is None or network.end_date is None:
            return True
        if network.end_date <= network.start_date:
            msg = "Network:%s invalid start_date=%s >= end_date=%s" % \
                    (network.code, network.start_date, network.end_date)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        return True

    # 111 Station:Epoch cannot be partly concurrent with any other Station:Epoch encompassed in parent Network:Epoch.
    def validate_rule_111(self, network):
        rule_code = '111'
        epoch_dict = {}
        overlapping = False
        for station in network.stations:
            key = station.code
            if key not in epoch_dict:
                epoch_dict[key] = []
            epoch_dict[key].append(epoch(station.start_date, station.end_date))

        for stn in epoch_dict:
            epochs = epoch_dict[stn]
            epochs.sort(key=lambda x: x.start_date, reverse=False)

            overlaps = overlapping_epochs(epochs)
            if overlaps:
                overlapping = True
                msg = "network:%s station:%s contains overlapping epochs" % (network.code, stn)
                self.errors.append((print_error(rule_code), msg))
                for overlap in overlaps:
                    self.errors.append("             epoch:[%s]" % overlap)
                self.return_codes.append(rule_code)
        if overlapping:
            return False
        else:
            return True

    # 112 Network:Epoch must encompass all subordinate Station:Epoch [Epoch=startDate-endDate]. [110, 210]
    def validate_rule_112(self, network):
        rule_code = '112'

        (earliest_start_date, latest_end_date) = get_first_start_last_end_dates(network.stations)

        passed = True

        if network.start_date is not None:
            if network.start_date > earliest_start_date:
                msg = "Network:%s start_date=%s > earliest station_start_date=%s" % \
                        (network.code, network.start_date, earliest_start_date)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False

        if network.end_date is not None:
            if network.end_date < latest_end_date:
                msg = "Network:%s end_date=%s < latest station_end_date=%s" % \
                        (network.code, network.end_date, latest_end_date)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False

        return passed

    # 112 Network:Epoch must encompass all subordinate Station:Epoch [Epoch=startDate-endDate]. [110, 210]
    def validate_rule_112_OLD(self, network):
        rule_code = '112'
        if network.start_date is None:
            msg = "Network:%s startDate not set --> Can't validate [112]" % network.code
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        (earliest_start_date, latest_end_date) = get_first_start_last_end_dates(network.stations)

        #MTH: if endDates are not set in the Station or Channel xml, latest_end_date will be None
        #     This could cause problems later if it's compare to another None object using '<'
        #if latest_end_date is None:
            #print("endDate is None!")

        if network.end_date is None:
            if network.start_date <= earliest_start_date:
                return True
            else:
                msg = "Network:%s start_date=%s > earliest station_start_date=%s" % \
                        (network.code, network.start_date, earliest_start_date)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                return False
        else:
            if network.start_date <= earliest_start_date and network.end_date >= latest_end_date:
                return True
            else:
                self.errors.append(print_error(rule_code))
                self.errors.append("        Network:%s does not encompass station epochs" % network.code)
                self.errors.append("        network epochs:[%s - %s]" % (network.start_date, network.end_date))
                self.errors.append("        station epochs:[%s - %s]" % (earliest_start_date, latest_end_date))
                self.return_codes.append(rule_code)
                return False

    # <-- Station Definition Errors -->

    # 201 Station:Code must be assigned a string consisting of 1-5 uppercase characters A-Z and or 
    #                  numeric characters 0-9.
    def validate_rule_201(self, station):
        rule_code = '201'
        if not valid_ascii(station.code, 1, 5):
            msg = "Invalid station code: [%s]" % station.code
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        return True

    # <-- Station Time Errors -->

    # 210 Station:startDate is required and must occur before Station:endDate 
    #                       if Station:endDate is available. [112, 212]
    def validate_rule_210(self, station):
        rule_code = '210'
        if station.start_date is None:
            msg = "station:%s startDate is not set" % station.code
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        if station.end_date and station.end_date <= station.start_date:
            msg = "station:%s start_date=[%s] >= end_date=[%s]" % \
                    (station.code, station.start_date, station.end_date)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        return True

    # 211 Channel:Epoch cannot be partly concurrent with any other Channel:Epoch encompassed 
    #                   in parent Station:Epoch.
    def validate_rule_211(self, station):
        rule_code = '211'
        pass_test = True
        if getattr(station, 'channels', None) is None or station.channels is None:
            msg = "station:%s contains 0 channels --> Can't validate [%s]" % (station.code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return True

        epoch_dict = {}
        for channel in station.channels:
            if channel.start_date is None:
                msg = "station:%s channel:%s.%s has empty start_date --> Can't sort/test epochs!" % \
                    (station.code, channel.location_code, channel.code)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
            else:
                key = "%s.%s" % (channel.location_code, channel.code)
                if key not in epoch_dict:
                    epoch_dict[key] = []
                epoch_dict[key].append(epoch(channel.start_date, channel.end_date))

        for chan in epoch_dict:
            epochs = epoch_dict[chan]
            epochs.sort(key=lambda x: x.start_date, reverse=False)
            overlaps = overlapping_epochs(epochs)
            if overlaps:
                pass_test = False
                msg = "station:%s channel:%s has overlapping epochs" % (station.code, chan)
                self.return_codes.append(rule_code)
                self.errors.append((print_error(rule_code), msg))
                self.errors.append("        Station:%s Chan:%s has overlapping epochs" % (station.code, chan))
                for overlap in overlaps:
                    self.errors.append("        epoch:[%s]" % overlap)

        return pass_test

    # <-- Station Position Errors -->

    # 212 Station:Epoch must encompass all subordinate Channel:Epoch [Epoch=startDate-endDate]. [210]
    def validate_rule_212(self, station):
        rule_code = '212'
        if station.start_date is None:
            msg = "station:%s startDate is not set --> Can't validate [%s]" % (station.code, rule_code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        if getattr(station, 'channels', None) is None or not station.channels:
            msg = "station:%s contains 0 channels --> Can't validate [%s]" % (station.code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        (earliest_start_date, latest_end_date) = get_first_start_last_end_dates(station.channels)

        passed = True

        if station.start_date > earliest_start_date:
            msg = "Station:%s start_date=%s > earliest channel_start_date=%s" % \
                    (station.code, station.start_date, earliest_start_date)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            passed = False

        if station.end_date is not None:
            if station.end_date < latest_end_date:
                msg = "Station:%s end_date=%s < latest channel_end_date=%s" % \
                        (station.code, station.end_date, latest_end_date)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False

        return passed

    # 212 Station:Epoch must encompass all subordinate Channel:Epoch [Epoch=startDate-endDate]. [210]
    def validate_rule_212_OLD(self, station):
        rule_code = '212'
        if station.start_date is None:
            msg = "station:%s startDate is not set --> Can't validate [%s]" % (station.code, rule_code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        if getattr(station, 'channels', None) is None or not station.channels:
            msg = "station:%s contains 0 channels --> Can't validate [%s]" % (station.code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        (earliest_start_date, latest_end_date) = get_first_start_last_end_dates(station.channels)

        if station.end_date is None:
            if station.start_date <= earliest_start_date:
                return True
            else:
                msg = "Station:%s start_date=%s >= earliest channel_start_date=%s" % \
                        (station.code, station.start_date, earliest_start_date)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                return False
        else:
            if station.start_date <= earliest_start_date and station.end_date >= latest_end_date:
                return True
            else:
                self.errors.append(print_error(rule_code))
                self.errors.append("        Station:%s does not encompass channel epochs" % station.code)
                self.errors.append("        station epochs:[%s - %s]" % (station.start_date, station.end_date))
                self.errors.append("        channel epochs:[%s - %s]" % (earliest_start_date, latest_end_date))
                self.return_codes.append(rule_code)
                return False

    # <-- Station Position Errors -->

    # MTH: Rules 220 & 221 are deprecated since station latitude/longitude are
    #      already checked in the FDSN schema

    # 220 Station:Latitude must be assigned a value between -90 and 90.
    def validate_rule_220(self, station):
        rule_code = '220'
        if station.latitude is None or station.latitude < -90. or station.latitude >= 90.:
            msg = "station:%s invalid latitude:%s" % (station.code, station.latitude)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        return True

    # 221 Station:Longitude must be assigned a value between -180 and 180.
    def validate_rule_221(self, station):
        rule_code = '221'
        if station.longitude is None or station.longitude < -180. or station.longitude > 180.:
            msg = "station:%s invalid longitude:%s" % (station.code, station.longitude)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        return True

    # 222 Station:Position must be within 1 km of all subordinate Channel:Position. Restrictions 'C1', 'C2'
    def validate_rule_222(self, station):
        rule_code = '222'

        passed = True

        for channel in station.channels:
            if getattr(channel, 'latitude', None) and getattr(channel, 'longitude', None):
                distaz = gps2dist_azimuth(station.latitude, station.longitude, channel.latitude, channel.longitude)
                dist = distaz[0]/1000.  # Dist in m --> km
                azim = distaz[1]
                baz  = distaz[2]

                if dist > 1.:
                    msg = "Station:%s Chan:%s - Channel is separated > 1km from Station!" % \
                            (station.code, channel.code)
                    self.errors.append((print_error(rule_code), msg))
                    self.return_codes.append(rule_code)
                    passed = False
            else:
                msg = "Station:%s Chan:%s - Channel does not have latitude/longitude set --> Can't validate Rule:%s" % \
                       (station.code, channel.code, rule_code)
                self.warnings.append((print_error(rule_code), msg))
                passed = False

        return passed

    # 223 Station:Elevation must be within 1 km of all subordinate Channel:Elevation.. Restrictions 'C1', 'C2'
    def validate_rule_223(self, station):
        rule_code = '223'

        passed = True

        for channel in station.channels:
            if getattr(channel, 'elevation', None):
                dist = np.abs(station.elevation - channel.elevation)
                if dist > 1.:
                    msg = "Station:%s Chan:%s - Channel depth is separated > 1km from Station!" % \
                            (station.code, channel.code)
                    self.warnings.append((print_error(rule_code), msg))
                    passed = False
            else:
                msg = "Station:%s Chan:%s - Channel does not have elevation set --> Can't validate Rule:%s" % \
                       (station.code, channel.code, rule_code)
                self.warnings.append((print_error(rule_code), msg))
                passed = False

        return passed

    # <-- Channel Definition Errors -->

    # 301 Channel:Code must be assigned a string consisting of 3 uppercase characters A-Z 
    #     and or numeric characters 0-9.
    def validate_rule_301(self, channel):
        rule_code = '301'
        if not valid_ascii(channel.code, 3, 3):
            msg = "Stn:%s chan:%s invalid channel code has len=%d != 3" % (self.station_code, channel.code, len(channel.code))
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        return True

    # 302 Channel:locationCode must be assigned a string consisting of 0-2 uppercase A-Z and numeric 0-9 
    #     characters OR 2 whitespace characters OR --.
    def validate_rule_302(self, channel):
        rule_code = '302'
        exceptions = ["  ", "--"]
        if getattr(channel, 'location_code', None) and not valid_ascii(channel.location_code, 0, 2):
            if channel.location_code in exceptions:
                pass
            else:
                msg = "Stn:%s chan:%s invalid channel_location code: [%s]" % (self.station_code, channel.code, channel.location_code)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                return False

        return True

    # 303 If CalibrationUnits are included then 
    #     CalibrationUnits:Name must be assigned a value from the IRIS StationXML Unit dictionary,
    #     case inconsistencies trigger warnings.
    def validate_rule_303(self, channel):
        rule_code = '303'
        if getattr(channel, 'calibration_units', None):
            cal_units = channel.calibration_units
            if cal_units not in unit_names:
                if cal_units.lower() in unit_names_lower:
                    msg = "Stn:%s Chan:%s calibration_units [%s] not in unit_names but lowercase is" % \
                        (self.station_code, channel.code, cal_units)
                    self.warnings.append((print_error(rule_code), msg))
                else:
                    msg = "Stn:%s Chan:%s calibration_units [%s] not in unit_names" % \
                        (self.station_code, channel.code, cal_units)
                    self.errors.append((print_error(rule_code), msg))
                    self.return_codes.append(rule_code)
                    return False

        return True

    # MTH: I'm not sure about this: seems like you could have a channel without a sensor
    # 304 Channel:Sensor:Description cannot be null.

    # 1. If we read in a stationxml with empty sensor description using read_inventory,
    #          then obspy will set sensor.description = "None" <str>
    # 2. If someone creates an inv on the fly with empty sensor description, 
    #          then obspy will set sensor.description = None <NoneType>
    # So we need to test for both

    # Jan 2020 Update to IRIS validation rules:
    # 304: Channel:Sensor:Description must be included and assigned a string consisting of 
    #    at least 1 case insensitive A-Z and numeric 0-9 characters.
    def validate_rule_304(self, channel):
        rule_code = '304'

        if getattr(channel, 'sensor', None) is None:
            msg = "Stn:%s Chan:%s does not have a sensor --> Can't validate rule %s" % \
                    (self.station_code, channel.code, rule_code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        description = getattr(channel.sensor, 'description', None)
        if description is None:
            msg = "Stn:%s Chan:%s has a sensor but sensor.description is None" % \
                    (self.station_code, channel.code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        elif description == 'None':
            msg = "Stn:%s Chan:%s has a sensor with sensor.description set to string='None' " % \
                    (self.station_code, channel.code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        elif len(re.sub("[a-zA-Z0-9]", '', description)) == 0:
            msg = "Stn:%s Chan:%s has a sensor but sensor.description = [%s] is invalid" % \
                    (self.station_code, channel.code, description)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        return True

    # 305 If Channel:SampleRate equals 0 or is not included then Response must not be included. [411, 421]
    def validate_rule_305(self, channel):
        rule_code = '305'
        if channel.response:
            if getattr(channel, 'sample_rate', None) is None:
                msg = "Stn:%s Chan:%s has a response but channel.sample_rate is empty" % \
                        (self.station_code, channel.code)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                return False

            if float(channel.sample_rate) == 0:
                msg = "Stn:%s Chan:%s has a response but channel.sample_rate == 0" % (self.station_code, channel.code)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                return False
        return True


    # <-- Channel Time Errors -->

    # 310 Channel:startDate must be included and must occur before Channel:endDate if included.
    def validate_rule_310(self, channel):
        rule_code = '310'
        if getattr(channel, 'start_date', None) is None:
            msg = "Stn:%s Chan:%s start_date not set" % (self.station_code, channel.code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        if getattr(channel, 'end_date', None) and channel.end_date <= channel.start_date:
            msg = "Stn:%s Chan:%s has start_date=[%s] >= end_date=[%s]" % \
                    (self.station_code, channel.code, channel.start_date, channel.end_date)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        return True

    # <-- Channel Position Errors -->
    # This section has been deprecated since these rules are already enforced by schema
    # Probably can't get here since obspy won't allow Channel(..) with bad lat/lon
    # 320 Channel:Latitude must be assigned a value between -90 and 90.

    # <-- Channel Orientation Errors -->
    # 320 If Channel:Code[2]==(H | L | M | N) THEN Channel:Azimuth and Channel:Dip must be included.
    def validate_rule_320(self, channel):
        rule_code = '320'
        if len(channel.code) != 3:
            msg = "Stn:%s Chan:%s != 3-chars--> Can't validate [%s]" % \
                    (self.station_code, channel.code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        if channel.code[1] in ['H', 'L', 'M', 'N'] and \
            (channel.azimuth is None or channel.dip is None):
            msg = "Stn:%s Chan:%s must have *both* azimuth and dip set!" % \
                    (self.station_code, channel.code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        return True

    # 321 If Channel:Code[2] == (H | L | M | N) then Stage[1]:InputUnit must equal *m/s* AND 
    #     Stage[Last]:OutputUnits must equal count*
    def validate_rule_321(self, channel):
        rule_code = '321'
        if len(channel.code) != 3:
            msg = "Stn:%s Chan:%s != 3-chars--> Can't validate [%s]" % \
                    (self.station_code, channel.code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        if not channel.response:
            msg = "Stn:%s Chan:%s has no response --> Can't validate rule:%s" % \
                    (self.station_code, channel.code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        if channel.code[1] in ['H', 'L', 'M', 'N']:
            stages = channel.response.response_stages
            if not stages:
                msg = "Stn:%s Chan:%s has response but no response_stages" % \
                    (self.station_code, channel.code)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                return False
            if stages[0].input_units != "m/s" or stages[-1].output_units != "count":
                msg = "Stn:%s Chan:%s response has 1st stage units=[%s] and last stage units=[%s]" % \
                    (self.station_code, channel.code, stages[0].input_units, stages[-1].output_units)
                self.warnings.append((print_error(rule_code), msg))
                #self.return_codes.append(rule_code)
                return False

        return True


    # Rules 330/331 are deprecated since these are already checked in FDSN Schema

    # 330 Azimuth must be assigned a value between 0 and 360.
    '''
    def validate_rule_330(self, channel):
        rule_code = '330'
        if channel.azimuth is None or channel.azimuth < 0 or channel.azimuth > 360:
            msg = "Stn:%s Chan:%s has invalid azimuth=[%s]" % (self.station_code, channel.code, channel.azimuth)
            #msg = "Chan:%s has invalid azimuth=[%s]" % (channel.code, channel.azimuth)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        return True
    '''

    # 331 Dip must be assigned a value between -90 and 90.
    '''
    def validate_rule_331(self, channel):
        rule_code = '331'
        if channel.dip is None or channel.dip < -90 or channel.dip > 90:
            msg = "Stn:%s Chan:%s has invalid dip=[%s]" % (self.station_code, channel.code, channel.dip)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False
        return True
    '''

    # N — Dip 0, Azimuth 0 degrees (Reversed: Dip 0, Azimuth 180 degrees).
    # E — Dip 0, Azimuth 90 degrees (Reversed: Dip 0, Azimuth 270 degrees).
    # Z — Dip -90, Azimuth 0 degrees (Reversed: Dip 90, Azimuth 0 degrees).

    # 332 If Channel:Code[LAST]==N then Channel:Azimuth must be assigned (>=355.0 or <=5.0)
    #    or (>=175.0 and <=185.0) 
    #    and Channel:Dip must be assigned (>=-5 AND <=5.0).
    def validate_rule_332(self, channel):
        rule_code = '332'
        if channel.code is None or len(channel.code) < 1:
            msg = "Stn:%s Missing channel.code --> Can't validate rule:%s" % \
                    (self.station_code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False
        if channel.azimuth is None or channel.dip is None:
            msg = "Stn:%s Chan:%s is missing either azimuth=[%s] or dip=[%s] --> Can't validate rule:%s" % \
                    (self.station_code, channel.code, channel.azimuth, channel.dip, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        if channel.code[-1] != 'N':
            return True

        #print("Check channel.dip=%s channel.azimuth=%s" % (channel.dip, channel.azimuth))
        if channel.dip >= -5. and channel.dip <= 5 and \
           ((channel.azimuth >= 355 and channel.azimuth <= 360) or \
            (channel.azimuth >= 0   and channel.azimuth <=  5) or \
            (channel.azimuth >= 175 and channel.azimuth <= 185)):
            return True
        else:
            msg = "Stn:%s Chan:%s Has incorrect dip:%f and/or azim:%f for a chan of type: '%s'\n" \
                    "Consider using Non-traditional Orthogonal Orientations:" % \
                    (self.station_code, channel.code, channel.dip, channel.azimuth, channel.code[2])
            #self.errors.append((print_error(rule_code), msg))
            #self.errors.append(non_traditional_orientations)
            #self.return_codes.append(rule_code)
            self.warnings.append((print_error(rule_code), msg))
            self.warnings.append(('',non_traditional_orientations))
            return False

    # 333 If Channel:Code[LAST]==E then Channel:Azimuth must be assigned (>=85.0 and <=95.0)
    #           or (>=265.0 and <=275.0) and Channel:Dip must be ASSIGNED (>=-5.0 and <=5.0).
    def validate_rule_333(self, channel):
        rule_code = '333'
        if channel.code is None or len(channel.code) < 1:
            msg = "Stn:%s Missing channel.code --> Can't validate rule:%s" % \
                    (self.station_code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False
        if channel.azimuth is None or channel.dip is None:
            msg = "Stn:%s Chan:%s is missing either azimuth=[%s] or dip=[%s] --> Can't validate rule:%s" % \
                    (self.station_code, channel.code, channel.azimuth, channel.dip, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        if channel.code[-1] != 'E':
            return True

        if channel.dip >= -5. and channel.dip <= 5 :
           if (channel.azimuth >= 85 and channel.azimuth <= 95) \
           or (channel.azimuth >= 265 and channel.azimuth <= 275.):
            return True

        else:
            msg = "Stn:%s Chan:%s Has incorrect dip:%f and/or azim:%f for a chan of type: '%s'\n" \
                    "Consider using Non-traditional Orthogonal Orientations:" % \
                    (self.station_code, channel.code, channel.dip, channel.azimuth, channel.code[2])
            self.warnings.append((print_error(rule_code), msg))
            self.warnings.append(('',non_traditional_orientations))
            #self.return_codes.append(rule_code)
            return False

    # 334 If Channel:Code[LAST]==Z then Channel:Azimuth must be assigned (>=355.0 or <=5.0)
    #        and Channel:Dip must be assigned (>=-85.0 and <=-90.0) or (>=85.0 and <=90.0).
    def validate_rule_334(self, channel):
        rule_code = '334'
        if channel.code is None or len(channel.code) < 1:
            msg = "Stn:%s Missing channel.code --> Can't validate rule:%s" % \
                    (self.station_code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False
        if channel.azimuth is None or channel.dip is None:
            msg = "Stn:%s Chan:%s is missing either azimuth=[%s] or dip=[%s] --> Can't validate rule:%s" % \
                    (self.station_code, channel.code, channel.azimuth, channel.dip, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        if channel.code[-1] != 'Z':
            return True

        if ((channel.azimuth >= 355 and channel.azimuth <= 360) or \
            (channel.azimuth >= 0   and channel.azimuth <=  5)) and \
           ((channel.dip >= 85. and channel.dip <= 90.) or \
            (channel.dip >= -90. and channel.dip <= -85.)):
            return True
        else:
            msg = "Stn:%s Chan:%s Has incorrect dip:%f and/or azim:%f for a chan of type: '%s'\n" \
                    "Consider using Non-traditional Orthogonal Orientations:" % \
                    (self.station_code, channel.code, channel.dip, channel.azimuth, channel.code[2])
            self.warnings.append((print_error(rule_code), msg))
            self.warnings.append(('', non_traditional_orientations))
            #self.return_codes.append(rule_code)
            return False

    # <-- Response Stage Errors -->

    def missing_response(self, channel, rule_code):
        if getattr(channel, 'response', None) is None or channel.response.response_stages is None:
            msg = "Stn:%s Chan:%s has no response stages--> Can't validate [%s]" % \
                    (self.station_code, channel.code, rule_code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)

    # 401 Stage:number must start at 1 and be sequential.
    def validate_rule_401(self, channel):
        rule_code = '401'
        if self.missing_response(channel, rule_code):
            return False

        stages = channel.response.response_stages

        if len(stages) == 0:
            msg = "Stn:%s Chan:%s has response with 0 stages --> Nothing left to check" % (self.station_code, channel.code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        sequence_numbers = []
        for stage in stages:
            sequence_numbers.append(stage.stage_sequence_number)
        increasing = all(i < j for i, j in zip(sequence_numbers, sequence_numbers[1:]))
        if increasing and sequence_numbers[0] == 1:
            return True
        else:
            msg = "Stn:%s Chan:%s invalid stage_sequence_numbers=[%s]" % (self.station_code, channel.code, sequence_numbers)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

    # 402 Stage[N]:InputUnits:Name and/or Stage[N]:OutputUnits:Name are not defined 
    #     in Unit name overview for IRIS StationXML validator. Capitalized unit names trigger warnings.
    def validate_rule_402(self, channel):
        rule_code = '402'
        if self.missing_response(channel, rule_code):
            return False

        stages = channel.response.response_stages

        passed = True
        for i, stage in enumerate(stages):
            i_stage = i+1
            input_units = getattr(stage, 'input_units', None)
            if input_units is None:
                msg = "Stn:%s Chan:%s stage:%d input_units is NOT set" % (self.station_code, channel.code, i_stage)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False
            else:
                if input_units not in unit_names:
                    if input_units.lower() in unit_names_lower:
                        msg = "Stn:%s Chan:%s stage:%d input_units [%s] not in unit_names but lowercase is" % \
                                (self.station_code, channel.code, i_stage, input_units)
                        self.warnings.append((print_error(rule_code), msg))
                    else:
                        msg = "Stn:%s Chan:%s stage:%d input_units [%s] not in unit_names" % \
                                (self.station_code, channel.code, i_stage, input_units)
                        self.errors.append((print_error(rule_code), msg))
                        self.return_codes.append(rule_code)
                        passed = False
            output_units = getattr(stage, 'output_units', None)
            if output_units is None:
                msg = "Stn:%s Chan:%s stage:%d output_units is NOT set" % (self.station_code, channel.code, i_stage)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False
            else:
                if output_units not in unit_names:
                    if output_units.lower() in unit_names_lower:
                        msg = "Stn:%s Chan:%s stage:%d output_units [%s] not in unit_names but lowercase is" % \
                                (self.station_code, channel.code, i_stage, output_units)
                        self.warnings.append((print_error(rule_code), msg))
                    else:
                        msg = "Stn:%s Chan:%s stage:%d output_units [%s] not in unit_names" % \
                                (self.station_code, channel.code, i_stage, output_units)
                        self.errors.append((print_error(rule_code), msg))
                        self.return_codes.append(rule_code)
                        passed = False
        return passed

    # 403 If length(Stage) > 1 then 
    #        Stage[N]:InputUnits:Name must equal Stage[N-1]:OutputUnits:Name.
    def validate_rule_403(self, channel):
        rule_code = '403'
        if self.missing_response(channel, rule_code):
            return False

        stages = channel.response.response_stages
        if len(stages) <= 1:
            return True

        passed = True
        for i in range(len(stages)-1):
            i_stage = i+1
            stage1 = stages[i]
            stage2 = stages[i+1]
            if stage2.input_units != stage1.output_units:
                msg = "Stn:%s Chan:%s stage[%d] output_units=%s != stage[%d] input_units=%s" % \
                        (self.station_code, channel.code, i_stage, stage1.output_units, i_stage+1, stage2.input_units)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False

        return passed

    # 404 If Stage[N]:PolesZeros:PzTransferFunctionType:Digital or Stage[N]:FIR or 
    #        Stage[N]:Coefficients:CfTransferFunctionType:DIGITAL are included 
    #        then Stage[N] must include Stage[N]:Decimation and Stage[N]:StageGain elements.
    def validate_rule_404(self, channel):
        rule_code = '404'
        if self.missing_response(channel, rule_code):
            return False

        stages = channel.response.response_stages

        passed = True
        for i, stage in enumerate(stages):
            if isinstance(stage, CoefficientsTypeResponseStage) or \
            isinstance(stage, FIRResponseStage) or \
            (isinstance(stage, PolesZerosResponseStage) \
                and stage.pz_transfer_function_type == "DIGITAL (Z-TRANSFORM)") :
                if stage.stage_gain and stage.decimation_factor and stage.decimation_factor >= 1:
                    pass
                else:
                    msg = "Stn:%s Chan:%s stage:%d missing stage_gain and/or decimation_factor" % (self.station_code, channel.code, i+1)
                    self.errors.append((print_error(rule_code), msg))
                    self.return_codes.append(rule_code)
                    passed = False
                    #print(msg)
        return passed

    # 405 Stage of type ResponseList cannot be the only stage included in a response. [420]
    def validate_rule_405(self, channel):
        rule_code = '405'
        if self.missing_response(channel, rule_code):
            return False

        stages = channel.response.response_stages
        if len(stages) == 1 and isinstance(stages[0], ResponseListResponseStage):
            self.errors.append(print_error(rule_code))
            self.return_codes.append(rule_code)
            return False

        return True

    # <-- ResponseType and StageGain Errors -->

    # 410 If InstrumentSensitivity is included then InstrumentSensitivity:Value must be 
    #     assigned a double > 0.0.
    def validate_rule_410(self, channel):
        rule_code = '410'
        if self.missing_response(channel, rule_code):
            return False

        response = channel.response
        if not response.instrument_sensitivity:
            return True

        if response.instrument_sensitivity.value > 0.:
            return True
        else:
            msg = "Stn:%s Chan:%s Missing response.instrument_sensitivity or instrument_sensitivity <= 0." % \
                    (self.station_code, channel.code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

    # 411 If InstrumentSensitivity is included then InstrumentSensitivity:Frequency must be assigned
    #        a double < Channel:SampleRate/2 [Nyquist Frequency].
    def validate_rule_411(self, channel):
        rule_code = '411'
        if self.missing_response(channel, rule_code):
            return False

        response = channel.response
        if not response.instrument_sensitivity:
            return True

        if getattr(channel, 'sample_rate', None) is None:
            msg = "Stn:%s Chan:%s has empty sample_rate --> Can't validate [%s]" % (self.station_code, channel.code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        if getattr(response.instrument_sensitivity, 'frequency', None) is None:
            msg = "Stn:%s Chan:%s response instrument_sensitivity missing frequency --> Can't validate [%s]" % (self.station_code, channel.code, rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        sensitivity = response.instrument_sensitivity
        chan_nyquist_freq = channel.sample_rate/2.
        if sensitivity.frequency > chan_nyquist_freq:
            msg = "Stn:%s Chan:%s instrument_sensitivity.freq:%f must be less than 1/2 of channel.sample_rate:%f" % \
                    (self.station_code, channel.code, sensitivity.frequency, channel.sample_rate)
            #self.errors.append((print_error(rule_code), msg))
            #self.return_codes.append(rule_code)
            self.warnings.append((print_error(rule_code), msg))
            return False

        return True

    # MTH: Unlikely that all stage_gain frequencies agree
    #      For now let's just compare sensitivities:
    #      The issue is that when obspy combines the NRL sensor (with gain/sensitivity calculated at one frequency)
    #          with the NRL datalogger (sensitivity at another frequency), it needs to adjust these to match.
    #          I think that for a non-flat sensor response, it recalculates the sensitivity away from the flat part
    #          so it changes from the value given in NRL.

    # 412 InstrumentSensitivity:Value must equal the product of all StageGain:Value if all StageGain:Frequency 
    #     are equal to InstrumentSensitivity:Frequency [Normalization Frequency]. [410]
    def validate_rule_412(self, channel):
        rule_code = '412'
        if self.missing_response(channel, rule_code):
            return False

        response = channel.response
        if not response.instrument_sensitivity:
            return True

        sensitivity = response.instrument_sensitivity

        passed = True
        overall_gain = 1.
        normalization_freq = set()
        for i, stage in enumerate(response.response_stages):
            if not getattr(stage, 'stage_gain', None) or stage.stage_gain <= 0:
                msg = "Stn:%s Chan:%s stage:%d has gain:%s --> Can't validate [%s]" % \
                        (self.station_code, channel.code, i, stage.stage_gain, rule_code)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False

            overall_gain *= stage.stage_gain
            normalization_freq.add(stage.stage_gain_frequency)

        if len(normalization_freq) == 1:
            diff = 100. * np.abs(overall_gain - sensitivity.value) / np.abs(sensitivity.value)
            # MTH: I'm interpreting overall sensitivity variation <5% as being "equal"
            if diff > 5.:
                msg = "channel:[%s] Calc stage0 gain:%f vs sensitivity:%f differs by > 5 percent" % \
                        (channel.code, overall_gain, sensitivity.value)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False

        return passed


    # 413 All Stages must include StageGain:Value assigned as a double > 0.0 and
    #     StageGain:Frequency assigned as a double.
    def validate_rule_413(self, channel):
        rule_code = '413'
        if self.missing_response(channel, rule_code):
            return False

        passed = True
        stages = channel.response.response_stages
        for i, stage in enumerate(stages):
            if stage.stage_gain is None or stage.stage_gain <= 0.:
                msg = "Chan:%s stage:%d invalid stage_gain=[%s]" % (channel.code, i+1, stage.stage_gain)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False
            try:
                float(stage.stage_gain_frequency)
            except ValueError:
                msg = "Chan:%s stage:%d invalid stage_gain_frequency=[%s]" % \
                        (channel.code, i+1, stage.stage_gain_frequency)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False

        return passed

    # 414 If Stage[N]:PolesZeros contains Zero:Real==0 and Zero:Imaginary==0 then 
    #     InstrumentSensitivity:Frequency cannot equal 0 and Stage[N]:StageGain:Frequency cannot equal 0.
    def validate_rule_414(self, channel):
        rule_code = '414'
        if self.missing_response(channel, rule_code):
            return False

        response = channel.response
        stages = channel.response.response_stages

        passed = True
        for i, stage in enumerate(stages):
            if isinstance(stage, PolesZerosResponseStage):
                zeros = stage.zeros
                for zero in zeros:
                    if zero.real == 0. and zero.imag == 0.:
                        if response.instrument_sensitivity.frequency is None or \
                           response.instrument_sensitivity.frequency == 0 or \
                           stage.stage_gain_frequency is None or stage.stage_gain_frequency == 0:
                            msg = "Chan:%s pz_stage contains zero at origin --> instrument_sensitivity_freq can't == 0" % \
                                   (channel.code)
                            self.errors.append((print_error(rule_code), msg))
                            self.return_codes.append(rule_code)
                            passed = False
        return passed

    # 415 Response must be of type InstrumentPolynomial if a Polynomial stage exist. [410,413,420]
    def validate_rule_415(self, channel):
        rule_code = '415'
        if self.missing_response(channel, rule_code):
            return False

        stages = channel.response.response_stages

        passed = True
        for i, stage in enumerate(stages):
            if isinstance(stage, PolynomialResponseStage) and channel.response.instrument_polynomial is None:
                msg = "Chan:%s response contains Polynomial stage but no InstrumentPolynomial block" % channel.code
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False

        return passed

    # 416 Response must include InstrumentSensitivity if no Polynomial stages are included.
    def validate_rule_416(self, channel):
        rule_code = '416'
        if self.missing_response(channel, rule_code):
            return False

        response = channel.response
        stages = response.response_stages

        has_polynomial_stage = False
        for i, stage in enumerate(stages):
            if isinstance(stage, PolynomialResponseStage):
                has_polynomial_stage = True
                break
        if not has_polynomial_stage and not getattr(response, 'instrument_sensitivity', None):
            msg = "Chan:%s response contains no polynomial stage but no InstrumentSensitivity block" % channel.code
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        return True

    # <-- Response Decimation Errors -->

    # 420 A Response must contain at least one instance of Response:Stage:Decimation. [404,405,414,415]
    def validate_rule_420(self, channel):
        rule_code = '420'
        if self.missing_response(channel, rule_code):
            return False
        stages = channel.response.response_stages

        decimation_stage_found = False
        for stage in stages:
            if getattr(stage, 'decimation_factor') and stage.decimation_factor >= 1:
                decimation_stage_found = True
                break
        if not decimation_stage_found:
            msg = "Chan:%s response contains 0 decimation stages" % channel.code
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        return True

    # 421 Stage[Final]:Decimation:InputSampleRate divided by Stage[Final]:Decimation:Factor 
    #                  must equal Channel:SampleRate. [305]
    def validate_rule_421(self, channel):
        rule_code = '421'
        if self.missing_response(channel, rule_code):
            return False

        if getattr(channel, 'sample_rate', None) is None:
            msg = "Chan:%s has empty sample_rate --> Can't validate [%s]" % (channel.code, rule_code)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        stages = channel.response.response_stages

        #print("Channel:%s has %d stages" % (channel.code, len(stages)))
        #for stage in stages:
            #print(stage)

        if stages[-1].decimation_factor is None or stages[-1].decimation_factor == 0.:
            msg = "Chan:%s final stage decimation_factor not set or == 0." % channel.code
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        expected_final_srate = stages[-1].decimation_input_sample_rate / stages[-1].decimation_factor
        if expected_final_srate != channel.sample_rate:
            msg = "Chan: [%s] expected_final_srate=%f != channel.sample_rate=%f" % \
                    (channel.code, expected_final_srate, channel.sample_rate)
            self.errors.append((print_error(rule_code), msg))
            self.return_codes.append(rule_code)
            return False

        return True


    # 422 Stage[N]:Decimation:InputSampleRate must equal Stage[N-1]:Decimation:InputSampleRate 
    #     divided by Stage[N-1]:Decimation:Factor.
    def validate_rule_422(self, channel):
        rule_code = '422'
        if self.missing_response(channel, rule_code):
            return False
        stages = channel.response.response_stages

        stages_with_decimation = []
        for stage in stages:
            if stage.decimation_input_sample_rate:
                stages_with_decimation.append(stage)

        passed = True
        for i in range(len(stages_with_decimation)-1):
            stage1 = stages_with_decimation[i]
            stage2 = stages_with_decimation[i+1]
            #print("Rule:%s chan:%s stage1:%d" % (rule_code, channel.code, i+1))
            if stage1.decimation_input_sample_rate is None:
                pass
            else:
                expected_input_sample_rate = stage1.decimation_input_sample_rate / stage1.decimation_factor
                if stage2.decimation_input_sample_rate != expected_input_sample_rate:
                    msg = "Chan:%s stage:%d has input_sr:%f != expected_sr:%f" % \
                        (channel.code, i+1, stage2.decimation_input_sample_rate, expected_input_sample_rate)
                    self.errors.append((print_error(rule_code), msg))
                    self.return_codes.append(rule_code)
                    passed = False

        return passed

    # 423 If Decimation and StageGain are included in Stage[N] then 
    #     PolesZeros or Coefficients or ResponseList or FIR must also be included in Stage[N].
    def validate_rule_423(self, channel):

        rule_code = '423'
        if self.missing_response(channel, rule_code):
            return False

        stages = channel.response.response_stages

        passed = True

        allowed_types = ['PolesZerosResponseStage',
                         'CoefficientsTypeResponseStage',
                         'FIRResponseStage',
                         'ResponseListResponseStage'
                         ]

        for i, stage in enumerate(stages):
            stage_type = type(stage).__name__
            if stage.decimation_input_sample_rate and stage_type not in allowed_types:
                msg = "Chan:%s response stage:%d has type:%s and input_sample_rate:%s --> decimation element is not allowed!" % \
                        (channel.code, i, type(stage).__name__, stage.decimation_input_sample_rate)
                #print(msg)
                self.errors.append((print_error(rule_code), msg))
                self.return_codes.append(rule_code)
                passed = False

        return passed

### End of stationxml_validator class

def get_first_start_last_end_dates(station_or_channel_list):

    # MTH: FDSN schema basenodetype startDate is *not* required!

    for elem in station_or_channel_list:
        if getattr(elem, 'start_date', None) is None:
            # This will get logged as [ERROR] for this station/channel/etc
            #logger.warning("Missing start_date --> Can't sort epochs")
            return None, None

    nepochs = len(station_or_channel_list)
    newlist = sorted(station_or_channel_list, key=lambda x: x.start_date, reverse=False)
    earliest_start = newlist[0].start_date

    slist = []
    for station_or_channel in station_or_channel_list:
        if getattr(station_or_channel, 'end_date', None) is not None:
            slist.append(station_or_channel)
    if slist:
        #newlist = sorted(station_or_channel_list, key=lambda x: x.end_date, reverse=True)
        newlist = sorted(slist, key=lambda x: x.end_date, reverse=True)
        latest_end = newlist[0].end_date
    else:
        latest_end = None

    return(earliest_start, latest_end)

def overlapping_epochs(epoch_list):

    overlap = False

    overlap_epochs = []

    for i in range(len(epoch_list)-1):

        epoch1 = epoch_list[i]
        epoch2 = epoch_list[i+1]

        if epoch1.start_date == epoch2.start_date:
            #print("Epochs have same start_date")
            overlap = True
        # epoch1 better be closed
        elif epoch1.end_date is None:
            #print("Earlier epoch not closed!")
            overlap = True
        # epoch1 close must precede epoch2 start
        elif epoch1.end_date > epoch2.start_date:
            #print("epoch1 end > epoch2 start")
            overlap = True

        if overlap:
            #print("Epoch:%s overlaps with epoch:%s" % (epoch1, epoch2))
            overlap_epochs.append(epoch1)
            overlap_epochs.append(epoch2)
            #return 1

    #return 0
    return overlap_epochs

def print_error(code):
    return "  [%s] %s" % (code, error_codes[code]['description'])
    #print("  [%s] %s" % (code, error_codes[code]['description']) )

def valid_ascii(string, min_len, max_len):
    # Network/Station/Channel codes must all be upper-case ascii chars

    #print("valid_ascii: string=[%s] len=%d min_len=%d max_len=%d" % (string, len(string), min_len, max_len))
    if isinstance(string, str) and len(string) >= min_len and len(string) <= max_len \
            and len(re.sub("[A-Z0-9]", '', string)) == 0:
                return 1
    else:
        return 0


def enforce_rule(channel, ERROR_CODE):

    # For future enforcement of any network/station exceptions:
    if not isinstance(channel, obspy.core.inventory.channel.Channel):
        return True

    restriction_list = error_codes[ERROR_CODE]['restrictions']

    for restriction_code in restriction_list:
        restriction_dict = restrictions[restriction_code]
        key = restriction_dict['key']
        if key == "Channel:Code":
            if channel.code in restriction_dict['immune']:
                #print("Chan:%s IS immune to rule:%s" % (channel.code, ERROR_CODE))
                return False

        # C2 : Channel:Type == "HEALTH", "FLAG", "MAINTENANCE" does not trigger Validation tests 
        #      that are subject to this restriction
        elif key == "Channel:Type":
            #print("Check channel type --> NOT implemented yet")
            pass
        elif key == "Response":
            if channel.response and channel.response.instrument_polynomial:
                #print("channel:%s has instrument polynomial --> Immune from rule:[%s]" % \
                      #(channel.code, ERROR_CODE))
                return False

    #print("Chan:%s is NOT immune to rule:%s" % (channel.code, ERROR_CODE))
    return True

levels = {'1':'network',
          '2':'station',
          '3':'channel',
          '4':'response'}

def get_string_from_level(n):
    fname = "get_string_from_level"
    if n not in levels.keys():
        s = ",".join(levels.keys())
        logger.error("%s: level must be in [%s]", (fname, s))
        return None
    return levels[n]

def get_rules(level='network'):

    if level not in levels.values():
        print("get_rules: Unknown level=[%s]" % level)
        return None

    k = list(levels.keys())[list(levels.values()).index(level)]

    rules = []
    for key in error_codes.keys():
        if key[0] == k:
            rules.append(key)

    # MTH: Hack to keep rule levels isolated
    #      IRIS Rule 321 is the ONLY level 3xx rule that requires
    #      the channel to have a response in order to validate
    #      ===> Move it to the Response level 4xx:
    if level == 'channel':
        rules = [rule for rule in rules if rule != '321']
    elif level == 'response':
        rules.append('321')

    return rules


def validate_stationxml_file_vs_rules(stationxml_file):
    '''
        Test input stationxml_file against all rules
    '''
    validator = stationxml_validator(stationxml_file)
    validator.validate_inventory()
    print("[ERRORS]:\n")
    for error in validator.errors:
        print(error)
    print("\n[WARNINGS]:\n")
    for warning in validator.warnings:
        print(warning)

    return

def stationxml_passes_rule(xmlfile, rule_code):
    '''
        Set up an xmlfile to pass against a single rule_code validator
    '''
    validator = stationxml_validator(xmlfile)
    func_name = "validator.validate_rule_%s" % rule_code

    passes = []
    networks = validator.inv.networks
    stations = []
    channels = []
    for network in networks:
        for station in network.stations:
            stations.append(station)
            for channel in station.channels:
                channels.append(channel)

    if rule_code[0] == '1':
        args = networks
    elif rule_code[0] == '2':
        args = stations
    elif rule_code[0] in ['3', '4']:
        args = channels

    for arg in args:
        passes.append(eval(func_name)(arg))

    if len(passes) == 1:
        passes = passes[0]

    return passes, validator.errors


def validate_iris_stationxml_examples_vs_rules():
    '''
        Loop through IRIS validation stationxmlfile examples (e.g., 'F1_304.xml')
            Test to see that file F?_XXX.xml correctly FAILS rule_code=XXX
            -or-
            Test to see that file P?_XXX.xml correctly PASSES rule_code=XXX
    '''

    test_dir = os.path.join(installation_dir(), 'iris_resources')

    for rule in error_codes.keys():
        files = test_xmls[rule]

        for fname in files:
            xmlfile = os.path.join(test_dir, fname)
            #code = fname[3:6]
            code = rule

            #print("Check file:%s against Rule:%s [file:%s]" % (fname, code, xmlfile))
            print("Check file:%s against Rule:%s" % (fname, code))
            if not os.path.isfile(xmlfile):
                print("******* Error: Can't find file:%s" % fname)
                continue

            passed, errors = stationxml_passes_rule(xmlfile, code)

            #for error in errors:
                #print(error)

            if fname[0:1] == 'P':
                if not passed:
                    print("ERROR: xmlfile=[%s] should have PASSED but failed" % fname)
                else:
                    print("SUCCESS: xmlfile=[%s] PASSED as expected" % fname)
            elif fname[0:1] == 'F':
                if passed:
                    print("ERROR: xmlfile=[%s] should NOT have PASSED!" % fname)
                else:
                    print("SUCCESS: xmlfile=[%s] FAILED as expected" % fname)


    return

def main():

    files = ['F1_305.xml', 'F2_305.xml']

    #for fname in files:
        #xmlfile = os.path.join(TEST_DIR, fname)
        #rule = fname[3:6]
        #passed, errors = stationxml_passes_rule(xmlfile, rule)
    validator = stationxml_validator('./iris_resources/F1_423.xml')
    validator.validate_rule('423')

    #print(inv)
    exit()

    TEST_DIR = "/Users/mth/mth/python_pkgs/stationxml-validator/src/test/resources/"
    validate_iris_stationxml_examples_vs_rules()
    exit()
    validate_stationxml_file_vs_rules(os.path.join(TEST_DIR, 'Validator_Pass.xml'))

if __name__ == "__main__":
    main()
