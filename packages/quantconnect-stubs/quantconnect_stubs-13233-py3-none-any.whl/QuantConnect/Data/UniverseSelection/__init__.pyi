import abc
import datetime
import typing
import warnings

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Fundamental
import QuantConnect.Data.UniverseSelection
import QuantConnect.Interfaces
import QuantConnect.Scheduling
import QuantConnect.Securities
import QuantConnect.Securities.Future
import QuantConnect.Securities.Option
import System
import System.Collections
import System.Collections.Concurrent
import System.Collections.Generic
import System.Collections.Specialized

QuantConnect_Data_UniverseSelection_FuncUniverse_T = typing.TypeVar("QuantConnect_Data_UniverseSelection_FuncUniverse_T")
QuantConnect_Data_UniverseSelection_ConstituentsUniverse_T = typing.TypeVar("QuantConnect_Data_UniverseSelection_ConstituentsUniverse_T")
QuantConnect_Data_UniverseSelection__EventContainer_Callable = typing.TypeVar("QuantConnect_Data_UniverseSelection__EventContainer_Callable")
QuantConnect_Data_UniverseSelection__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Data_UniverseSelection__EventContainer_ReturnType")


class UniverseSettings(System.Object):
    """Defines settings required when adding a subscription"""

    @property
    def Resolution(self) -> QuantConnect.Resolution:
        """The resolution to be used"""
        ...

    @Resolution.setter
    def Resolution(self, value: QuantConnect.Resolution):
        """The resolution to be used"""
        ...

    @property
    def Leverage(self) -> float:
        """The leverage to be used"""
        ...

    @Leverage.setter
    def Leverage(self, value: float):
        """The leverage to be used"""
        ...

    @property
    def FillForward(self) -> bool:
        """True to fill data forward, false otherwise"""
        ...

    @FillForward.setter
    def FillForward(self, value: bool):
        """True to fill data forward, false otherwise"""
        ...

    @property
    def ExtendedMarketHours(self) -> bool:
        """True to allow extended market hours data, false otherwise"""
        ...

    @ExtendedMarketHours.setter
    def ExtendedMarketHours(self, value: bool):
        """True to allow extended market hours data, false otherwise"""
        ...

    @property
    def MinimumTimeInUniverse(self) -> datetime.timedelta:
        """
        Defines the minimum amount of time a security must be in
        the universe before being removed.
        """
        ...

    @MinimumTimeInUniverse.setter
    def MinimumTimeInUniverse(self, value: datetime.timedelta):
        """
        Defines the minimum amount of time a security must be in
        the universe before being removed.
        """
        ...

    @property
    def DataNormalizationMode(self) -> QuantConnect.DataNormalizationMode:
        """Defines how universe data is normalized before being send into the algorithm"""
        ...

    @DataNormalizationMode.setter
    def DataNormalizationMode(self, value: QuantConnect.DataNormalizationMode):
        """Defines how universe data is normalized before being send into the algorithm"""
        ...

    @property
    def DataMappingMode(self) -> QuantConnect.DataMappingMode:
        """Defines how universe data is mapped together"""
        ...

    @DataMappingMode.setter
    def DataMappingMode(self, value: QuantConnect.DataMappingMode):
        """Defines how universe data is mapped together"""
        ...

    @property
    def ContractDepthOffset(self) -> int:
        """
        The continuous contract desired offset from the current front month.
        For example, 0 (default) will use the front month, 1 will use the back month contra
        """
        ...

    @ContractDepthOffset.setter
    def ContractDepthOffset(self, value: int):
        """
        The continuous contract desired offset from the current front month.
        For example, 0 (default) will use the front month, 1 will use the back month contra
        """
        ...

    @property
    def SubscriptionDataTypes(self) -> System.Collections.Generic.List[System.Tuple[typing.Type, QuantConnect.TickType]]:
        """Allows a universe to specify which data types to add for a selected symbol"""
        ...

    @SubscriptionDataTypes.setter
    def SubscriptionDataTypes(self, value: System.Collections.Generic.List[System.Tuple[typing.Type, QuantConnect.TickType]]):
        """Allows a universe to specify which data types to add for a selected symbol"""
        ...

    @typing.overload
    def __init__(self, resolution: QuantConnect.Resolution, leverage: float, fillForward: bool, extendedMarketHours: bool, minimumTimeInUniverse: datetime.timedelta, dataNormalizationMode: QuantConnect.DataNormalizationMode = ..., dataMappingMode: QuantConnect.DataMappingMode = ..., contractDepthOffset: int = 0) -> None:
        """
        Initializes a new instance of the UniverseSettings class
        
        :param resolution: The resolution
        :param leverage: The leverage to be used
        :param fillForward: True to fill data forward, false otherwise
        :param extendedMarketHours: True to allow extended market hours data, false otherwise
        :param minimumTimeInUniverse: Defines the minimum amount of time a security must remain in the universe before being removed
        :param dataNormalizationMode: Defines how universe data is normalized before being send into the algorithm
        :param dataMappingMode: The contract mapping mode to use for the security
        :param contractDepthOffset: The continuous contract desired offset from the current front month. For example, 0 (default) will use the front month, 1 will use the back month contract
        """
        ...

    @typing.overload
    def __init__(self, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings) -> None:
        """Initializes a new instance of the UniverseSettings class"""
        ...


class BaseDataCollection(QuantConnect.Data.BaseData, typing.Iterable[QuantConnect.Data.BaseData]):
    """This type exists for transport of data as a single packet"""

    @property
    def Data(self) -> System.Collections.Generic.List[QuantConnect.Data.BaseData]:
        """Gets the data list"""
        ...

    @Data.setter
    def Data(self, value: System.Collections.Generic.List[QuantConnect.Data.BaseData]):
        """Gets the data list"""
        ...

    @property
    def EndTime(self) -> datetime.datetime:
        """Gets or sets the end time of this data"""
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """Gets or sets the end time of this data"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Initializes a new default instance of the BaseDataCollection c;ass"""
        ...

    @typing.overload
    def __init__(self, time: typing.Union[datetime.datetime, datetime.date], symbol: typing.Union[QuantConnect.Symbol, str], data: System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData] = None) -> None:
        """
        Initializes a new instance of the BaseDataCollection class
        
        :param time: The time of this data
        :param symbol: A common identifier for all data in this packet
        :param data: The data to add to this collection
        """
        ...

    @typing.overload
    def __init__(self, time: typing.Union[datetime.datetime, datetime.date], endTime: typing.Union[datetime.datetime, datetime.date], symbol: typing.Union[QuantConnect.Symbol, str], data: System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData] = None) -> None:
        """
        Initializes a new instance of the BaseDataCollection class
        
        :param time: The start time of this data
        :param endTime: The end time of this data
        :param symbol: A common identifier for all data in this packet
        :param data: The data to add to this collection
        """
        ...

    @typing.overload
    def __init__(self, time: typing.Union[datetime.datetime, datetime.date], endTime: typing.Union[datetime.datetime, datetime.date], symbol: typing.Union[QuantConnect.Symbol, str], data: System.Collections.Generic.List[QuantConnect.Data.BaseData]) -> None:
        """
        Initializes a new instance of the BaseDataCollection class
        
        :param time: The start time of this data
        :param endTime: The end time of this data
        :param symbol: A common identifier for all data in this packet
        :param data: The data to add to this collection
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Return a new instance clone of this object, used in fill forward
        
        :returns: A clone of the current object.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """
        Returns an IEnumerator for this enumerable Object.  The enumerator provides
        a simple way to access all the contents of a collection.
        """
        ...

    @typing.overload
    def GetEnumerator(self) -> System.Collections.IEnumerator:
        """
        Returns an IEnumerator for this enumerable Object.  The enumerator provides
        a simple way to access all the contents of a collection.
        """
        ...


class ETFConstituentData(QuantConnect.Data.BaseData):
    """ETF constituent data"""

    @property
    def LastUpdate(self) -> typing.Optional[datetime.datetime]:
        """Time of the previous ETF constituent data update"""
        ...

    @LastUpdate.setter
    def LastUpdate(self, value: typing.Optional[datetime.datetime]):
        """Time of the previous ETF constituent data update"""
        ...

    @property
    def Weight(self) -> typing.Optional[float]:
        """The percentage of the ETF allocated to this constituent"""
        ...

    @Weight.setter
    def Weight(self, value: typing.Optional[float]):
        """The percentage of the ETF allocated to this constituent"""
        ...

    @property
    def SharesHeld(self) -> typing.Optional[float]:
        """Number of shares held in the ETF"""
        ...

    @SharesHeld.setter
    def SharesHeld(self, value: typing.Optional[float]):
        """Number of shares held in the ETF"""
        ...

    @property
    def MarketValue(self) -> typing.Optional[float]:
        """Market value of the current asset held in U.S. dollars"""
        ...

    @MarketValue.setter
    def MarketValue(self, value: typing.Optional[float]):
        """Market value of the current asset held in U.S. dollars"""
        ...

    @property
    def Period(self) -> datetime.timedelta:
        """Period of the data"""
        ...

    @Period.setter
    def Period(self, value: datetime.timedelta):
        """Period of the data"""
        ...

    @property
    def EndTime(self) -> datetime.datetime:
        """Time that the data became available to use"""
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """Time that the data became available to use"""
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Creates a copy of the instance
        
        :returns: Clone of the instance.
        """
        ...

    def DataTimeZone(self) -> typing.Any:
        """
        Specifies the data time zone for this data type. This is useful for custom data types
        
        :returns: The DateTimeZone of this data type.
        """
        ...

    def DefaultResolution(self) -> int:
        """
        Gets the default resolution for this data and security type
        
        :returns: This method returns the int value of a member of the QuantConnect.Resolution enum.
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the URL string source of the file. This will be converted to a stream
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: String URL of source file.
        """
        ...

    def IsSparseData(self) -> bool:
        """
        Indicates that the data set is expected to be sparse
        
        :returns: True if the data set represented by this type is expected to be sparse.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects. Each data type creates its own factory method, and returns a new instance of the object
        each time it is called.
        
        :param config: Subscription data config setup object
        :param line: Line of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Instance of the T:BaseData object generated by this line of the CSV.
        """
        ...

    def RequiresMapping(self) -> bool:
        """
        Indicates if there is support for mapping
        
        :returns: True indicates mapping should be used.
        """
        ...

    def SupportedResolutions(self) -> System.Collections.Generic.List[QuantConnect.Resolution]:
        """Gets the supported resolution for this data and security type"""
        ...


class SubscriptionRequest(QuantConnect.Data.BaseDataRequest):
    """Defines the parameters required to add a subscription to a data feed."""

    @property
    def IsUniverseSubscription(self) -> bool:
        """Gets true if the subscription is a universe"""
        ...

    @property
    def Universe(self) -> QuantConnect.Data.UniverseSelection.Universe:
        """Gets the universe this subscription resides in"""
        ...

    @property
    def Security(self) -> QuantConnect.Securities.Security:
        """Gets the security. This is the destination of data for non-internal subscriptions."""
        ...

    @property
    def Configuration(self) -> QuantConnect.Data.SubscriptionDataConfig:
        """Gets the subscription configuration. This defines how/where to read the data."""
        ...

    @property
    def TradableDays(self) -> System.Collections.Generic.IEnumerable[datetime.datetime]:
        """Gets the tradable days specified by this request, in the security's data time zone"""
        ...

    @typing.overload
    def __init__(self, isUniverseSubscription: bool, universe: QuantConnect.Data.UniverseSelection.Universe, security: QuantConnect.Securities.Security, configuration: QuantConnect.Data.SubscriptionDataConfig, startTimeUtc: typing.Union[datetime.datetime, datetime.date], endTimeUtc: typing.Union[datetime.datetime, datetime.date]) -> None:
        """Initializes a new instance of the SubscriptionRequest class"""
        ...

    @typing.overload
    def __init__(self, template: QuantConnect.Data.UniverseSelection.SubscriptionRequest, isUniverseSubscription: typing.Optional[bool] = None, universe: QuantConnect.Data.UniverseSelection.Universe = None, security: QuantConnect.Securities.Security = None, configuration: QuantConnect.Data.SubscriptionDataConfig = None, startTimeUtc: typing.Optional[datetime.datetime] = None, endTimeUtc: typing.Optional[datetime.datetime] = None) -> None:
        """Initializes a new instance of the SubscriptionRequest class"""
        ...


class Universe(System.Object, System.IDisposable, metaclass=abc.ABCMeta):
    """Provides a base class for all universes to derive from."""

    class UnchangedUniverse(System.Object, typing.Iterable[QuantConnect.Symbol]):
        """
        Provides a value to indicate that no changes should be made to the universe.
        This value is intended to be returned by reference via Universe.SelectSymbols
        """

        Instance: QuantConnect.Data.UniverseSelection.Universe.UnchangedUniverse = ...
        """Read-only instance of the UnchangedUniverse value"""

        @typing.overload
        def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect.Symbol]:
            ...

        @typing.overload
        def GetEnumerator(self) -> System.Collections.Generic.IEnumerator[str]:
            ...

        @typing.overload
        def GetEnumerator(self) -> System.Collections.IEnumerator:
            ...

    class Member(System.Object):
        """Member of the Universe"""

        @property
        def Added(self) -> datetime.datetime:
            """DateTime when added"""
            ...

        @property
        def Security(self) -> QuantConnect.Securities.Security:
            """The security that was added"""
            ...

        def __init__(self, added: typing.Union[datetime.datetime, datetime.date], security: QuantConnect.Securities.Security) -> None:
            """
            Initialize a new member for the universe
            
            :param added: DateTime added
            :param security: Security to add
            """
            ...

    class SelectionEventArgs(System.EventArgs):
        """Event fired when the universe selection changes"""

        @property
        def CurrentSelection(self) -> System.Collections.Generic.HashSet[QuantConnect.Symbol]:
            """The current universe selection"""
            ...

        def __init__(self, currentSelection: System.Collections.Generic.HashSet[QuantConnect.Symbol]) -> None:
            """Creates a new instance"""
            ...

    Unchanged: QuantConnect.Data.UniverseSelection.Universe.UnchangedUniverse = ...
    """Gets a value indicating that no change to the universe should be made"""

    @property
    def Securities(self) -> System.Collections.Concurrent.ConcurrentDictionary[QuantConnect.Symbol, QuantConnect.Data.UniverseSelection.Universe.Member]:
        """Gets the internal security collection used to define membership in this universe"""
        ...

    @Securities.setter
    def Securities(self, value: System.Collections.Concurrent.ConcurrentDictionary[QuantConnect.Symbol, QuantConnect.Data.UniverseSelection.Universe.Member]):
        """Gets the internal security collection used to define membership in this universe"""
        ...

    @property
    def SelectionChanged(self) -> _EventContainer[typing.Callable[[System.Object, System.EventArgs], None], None]:
        """Event fired when the universe selection has changed"""
        ...

    @SelectionChanged.setter
    def SelectionChanged(self, value: _EventContainer[typing.Callable[[System.Object, System.EventArgs], None], None]):
        """Event fired when the universe selection has changed"""
        ...

    @property
    def SecurityType(self) -> int:
        """
        Gets the security type of this universe
        
        This property contains the int value of a member of the QuantConnect.SecurityType enum.
        """
        ...

    @property
    def Market(self) -> str:
        """Gets the market of this universe"""
        ...

    @property
    def DisposeRequested(self) -> bool:
        """Flag indicating if disposal of this universe has been requested"""
        ...

    @DisposeRequested.setter
    def DisposeRequested(self, value: bool):
        """Flag indicating if disposal of this universe has been requested"""
        ...

    @property
    @abc.abstractmethod
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the settings used for subscriptions added for this universe"""
        ...

    @property
    def Configuration(self) -> QuantConnect.Data.SubscriptionDataConfig:
        """Gets the configuration used to get universe data"""
        ...

    @Configuration.setter
    def Configuration(self, value: QuantConnect.Data.SubscriptionDataConfig):
        """Gets the configuration used to get universe data"""
        ...

    @property
    def Members(self) -> System.Collections.Generic.Dictionary[QuantConnect.Symbol, QuantConnect.Securities.Security]:
        """
        Gets the current listing of members in this universe. Modifications
        to this dictionary do not change universe membership.
        """
        ...

    def __init__(self, config: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """
        Initializes a new instance of the Universe class
        
        This method is protected.
        
        :param config: The configuration used to source data for this universe
        """
        ...

    def CanRemoveMember(self, utcTime: typing.Union[datetime.datetime, datetime.date], security: QuantConnect.Securities.Security) -> bool:
        """
        Determines whether or not the specified security can be removed from
        this universe. This is useful to prevent securities from being taken
        out of a universe before the algorithm has had enough time to make
        decisions on the security
        
        :param utcTime: The current utc time
        :param security: The security to check if its ok to remove
        :returns: True if we can remove the security, false otherwise.
        """
        ...

    def ContainsMember(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Determines whether or not the specified symbol is currently a member of this universe
        
        :param symbol: The symbol whose membership is to be checked
        :returns: True if the specified symbol is part of this universe, false otherwise.
        """
        ...

    def CreateSecurity(self, symbol: typing.Union[QuantConnect.Symbol, str], algorithm: QuantConnect.Interfaces.IAlgorithm, marketHoursDatabase: QuantConnect.Securities.MarketHoursDatabase, symbolPropertiesDatabase: QuantConnect.Securities.SymbolPropertiesDatabase) -> QuantConnect.Securities.Security:
        """
        Creates and configures a security for the specified symbol
        
        CreateSecurity is obsolete and will not be called. The system will create the required Securities based on selected symbols
        
        :param symbol: The symbol of the security to be created
        :param algorithm: The algorithm instance
        :param marketHoursDatabase: The market hours database
        :param symbolPropertiesDatabase: The symbol properties database
        :returns: The newly initialized security object.
        """
        warnings.warn("CreateSecurity is obsolete and will not be called. The system will create the required Securities based on selected symbols", DeprecationWarning)

    def Dispose(self) -> None:
        """Marks this universe as disposed and ready to remove all child subscriptions"""
        ...

    @typing.overload
    def GetSubscriptionRequests(self, security: QuantConnect.Securities.Security, currentTimeUtc: typing.Union[datetime.datetime, datetime.date], maximumEndTimeUtc: typing.Union[datetime.datetime, datetime.date], subscriptionService: QuantConnect.Interfaces.ISubscriptionDataConfigService) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]:
        """
        Gets the subscription requests to be added for the specified security
        
        :param security: The security to get subscriptions for
        :param currentTimeUtc: The current time in utc. This is the frontier time of the algorithm
        :param maximumEndTimeUtc: The max end time
        :param subscriptionService: Instance which implements ISubscriptionDataConfigService interface
        :returns: All subscriptions required by this security.
        """
        ...

    @typing.overload
    def GetSubscriptionRequests(self, security: QuantConnect.Securities.Security, currentTimeUtc: typing.Union[datetime.datetime, datetime.date], maximumEndTimeUtc: typing.Union[datetime.datetime, datetime.date]) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]:
        """
        Gets the subscription requests to be added for the specified security
        
        This overload is obsolete and will not be called. It was not capable of creating new SubscriptionDataConfig due to lack of information
        
        :param security: The security to get subscriptions for
        :param currentTimeUtc: The current time in utc. This is the frontier time of the algorithm
        :param maximumEndTimeUtc: The max end time
        :returns: All subscriptions required by this security.
        """
        ...

    def OnSelectionChanged(self, selection: System.Collections.Generic.HashSet[QuantConnect.Symbol] = None) -> None:
        """
        Event invocator for the SelectionChanged event
        
        This method is protected.
        
        :param selection: The current universe selection
        """
        ...

    def PerformSelection(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs universe selection using the data specified
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs universe selection using the data specified
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...


class OptionChainUniverse(QuantConnect.Data.UniverseSelection.Universe):
    """Defines a universe for a single option chain"""

    @property
    def Option(self) -> QuantConnect.Securities.Option.Option:
        """The canonical option chain security"""
        ...

    @property
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the settings used for subscriptons added for this universe"""
        ...

    def __init__(self, option: QuantConnect.Securities.Option.Option, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, liveMode: bool) -> None:
        """
        Initializes a new instance of the OptionChainUniverse class
        
        :param option: The canonical option chain security
        :param universeSettings: The universe settings to be used for new subscriptions
        :param liveMode: True if we're running in live mode, false for backtest mode
        """
        ...

    def CanRemoveMember(self, utcTime: typing.Union[datetime.datetime, datetime.date], security: QuantConnect.Securities.Security) -> bool:
        """
        Determines whether or not the specified security can be removed from
        this universe. This is useful to prevent securities from being taken
        out of a universe before the algorithm has had enough time to make
        decisions on the security
        
        :param utcTime: The current utc time
        :param security: The security to check if its ok to remove
        :returns: True if we can remove the security, false otherwise.
        """
        ...

    def GetSubscriptionRequests(self, security: QuantConnect.Securities.Security, currentTimeUtc: typing.Union[datetime.datetime, datetime.date], maximumEndTimeUtc: typing.Union[datetime.datetime, datetime.date], subscriptionService: QuantConnect.Interfaces.ISubscriptionDataConfigService) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]:
        """
        Gets the subscription requests to be added for the specified security
        
        :param security: The security to get subscriptions for
        :param currentTimeUtc: The current time in utc. This is the frontier time of the algorithm
        :param maximumEndTimeUtc: The max end time
        :param subscriptionService: Instance which implements ISubscriptionDataConfigService interface
        :returns: All subscriptions required by this security.
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs universe selection using the data specified
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...


class ITimeTriggeredUniverse(metaclass=abc.ABCMeta):
    """
    A universe implementing this interface will NOT use it's SubscriptionDataConfig to generate data
    that is used to 'pulse' the universe selection function -- instead, the times output by
    GetTriggerTimes are used to 'pulse' the universe selection function WITHOUT data.
    """

    def GetTriggerTimes(self, startTimeUtc: typing.Union[datetime.datetime, datetime.date], endTimeUtc: typing.Union[datetime.datetime, datetime.date], marketHoursDatabase: QuantConnect.Securities.MarketHoursDatabase) -> System.Collections.Generic.IEnumerable[datetime.datetime]:
        """
        Returns an enumerator that defines when this user defined universe will be invoked
        
        :returns: An enumerator of DateTime that defines when this universe will be invoked.
        """
        ...


class ScheduledUniverse(QuantConnect.Data.UniverseSelection.Universe, QuantConnect.Data.UniverseSelection.ITimeTriggeredUniverse):
    """Defines a user that is fired based on a specified IDateRule and ITimeRule"""

    @property
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the settings used for subscriptons added for this universe"""
        ...

    @typing.overload
    def __init__(self, timeZone: typing.Any, dateRule: QuantConnect.Scheduling.IDateRule, timeRule: QuantConnect.Scheduling.ITimeRule, selector: typing.Callable[[datetime.datetime], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]], settings: QuantConnect.Data.UniverseSelection.UniverseSettings = None) -> None:
        """
        Initializes a new instance of the ScheduledUniverse class
        
        :param timeZone: The time zone the date/time rules are in
        :param dateRule: Date rule defines what days the universe selection function will be invoked
        :param timeRule: Time rule defines what times on each day selected by date rule the universe selection function will be invoked
        :param selector: Selector function accepting the date time firing time and returning the universe selected symbols
        :param settings: Universe settings for subscriptions added via this universe, null will default to algorithm's universe settings
        """
        ...

    @typing.overload
    def __init__(self, dateRule: QuantConnect.Scheduling.IDateRule, timeRule: QuantConnect.Scheduling.ITimeRule, selector: typing.Callable[[datetime.datetime], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]], settings: QuantConnect.Data.UniverseSelection.UniverseSettings = None) -> None:
        """
        Initializes a new instance of the ScheduledUniverse class
        
        :param dateRule: Date rule defines what days the universe selection function will be invoked
        :param timeRule: Time rule defines what times on each day selected by date rule the universe selection function will be invoked
        :param selector: Selector function accepting the date time firing time and returning the universe selected symbols
        :param settings: Universe settings for subscriptions added via this universe, null will default to algorithm's universe settings
        """
        ...

    @typing.overload
    def __init__(self, timeZone: typing.Any, dateRule: QuantConnect.Scheduling.IDateRule, timeRule: QuantConnect.Scheduling.ITimeRule, selector: typing.Any, settings: QuantConnect.Data.UniverseSelection.UniverseSettings = None) -> None:
        """
        Initializes a new instance of the ScheduledUniverse class
        
        :param timeZone: The time zone the date/time rules are in
        :param dateRule: Date rule defines what days the universe selection function will be invoked
        :param timeRule: Time rule defines what times on each day selected by date rule the universe selection function will be invoked
        :param selector: Selector function accepting the date time firing time and returning the universe selected symbols
        :param settings: Universe settings for subscriptions added via this universe, null will default to algorithm's universe settings
        """
        ...

    @typing.overload
    def __init__(self, dateRule: QuantConnect.Scheduling.IDateRule, timeRule: QuantConnect.Scheduling.ITimeRule, selector: typing.Any, settings: QuantConnect.Data.UniverseSelection.UniverseSettings = None) -> None:
        """
        Initializes a new instance of the ScheduledUniverse class
        
        :param dateRule: Date rule defines what days the universe selection function will be invoked
        :param timeRule: Time rule defines what times on each day selected by date rule the universe selection function will be invoked
        :param selector: Selector function accepting the date time firing time and returning the universe selected symbols
        :param settings: Universe settings for subscriptions added via this universe, null will default to algorithm's universe settings
        """
        ...

    def GetTriggerTimes(self, startTimeUtc: typing.Union[datetime.datetime, datetime.date], endTimeUtc: typing.Union[datetime.datetime, datetime.date], marketHoursDatabase: QuantConnect.Securities.MarketHoursDatabase) -> System.Collections.Generic.IEnumerable[datetime.datetime]:
        """
        Get an enumerator of UTC DateTimes that defines when this universe will be invoked
        
        :param startTimeUtc: The start time of the range in UTC
        :param endTimeUtc: The end time of the range in UTC
        :returns: An enumerator of UTC DateTimes that defines when this universe will be invoked.
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs universe selection using the data specified
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...


class FuturesChainUniverse(QuantConnect.Data.UniverseSelection.Universe):
    """Defines a universe for a single futures chain"""

    @property
    def Future(self) -> QuantConnect.Securities.Future.Future:
        """The canonical future chain security"""
        ...

    @property
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the settings used for subscriptons added for this universe"""
        ...

    def __init__(self, future: QuantConnect.Securities.Future.Future, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings) -> None:
        """
        Initializes a new instance of the FuturesChainUniverse class
        
        :param future: The canonical future chain security
        :param universeSettings: The universe settings to be used for new subscriptions
        """
        ...

    def CanRemoveMember(self, utcTime: typing.Union[datetime.datetime, datetime.date], security: QuantConnect.Securities.Security) -> bool:
        """
        Determines whether or not the specified security can be removed from
        this universe. This is useful to prevent securities from being taken
        out of a universe before the algorithm has had enough time to make
        decisions on the security
        
        :param utcTime: The current utc time
        :param security: The security to check if its ok to remove
        :returns: True if we can remove the security, false otherwise.
        """
        ...

    def GetSubscriptionRequests(self, security: QuantConnect.Securities.Security, currentTimeUtc: typing.Union[datetime.datetime, datetime.date], maximumEndTimeUtc: typing.Union[datetime.datetime, datetime.date], subscriptionService: QuantConnect.Interfaces.ISubscriptionDataConfigService) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]:
        """
        Gets the subscription requests to be added for the specified security
        
        :param security: The security to get subscriptions for
        :param currentTimeUtc: The current time in utc. This is the frontier time of the algorithm
        :param maximumEndTimeUtc: The max end time
        :param subscriptionService: Instance which implements ISubscriptionDataConfigService interface
        :returns: All subscriptions required by this security.
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs universe selection using the data specified
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...


class FuncUniverse(typing.Generic[QuantConnect_Data_UniverseSelection_FuncUniverse_T], QuantConnect.Data.UniverseSelection.Universe):
    """Provides a functional implementation of Universe"""

    @property
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the settings used for subscriptons added for this universe"""
        ...

    @typing.overload
    def __init__(self, configuration: QuantConnect.Data.SubscriptionDataConfig, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, universeSelector: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect_Data_UniverseSelection_FuncUniverse_T]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]]) -> None:
        """
        Initializes a new instance of the FuncUniverse{T} class
        
        :param configuration: The configuration used to resolve the data for universe selection
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param universeSelector: Returns the symbols that should be included in the universe
        """
        ...

    @typing.overload
    def __init__(self, configuration: QuantConnect.Data.SubscriptionDataConfig, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, universeSelector: typing.Any) -> None:
        """
        Initializes a new instance of the FuncUniverse{T} class for a filter function loaded from Python
        
        :param configuration: The configuration used to resolve the data for universe selection
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param universeSelector: Function that returns the symbols that should be included in the universe
        """
        ...

    @typing.overload
    def __init__(self, configuration: QuantConnect.Data.SubscriptionDataConfig, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, universeSelector: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]]) -> None:
        """
        Initializes a new instance of the FuncUniverse class
        
        :param configuration: The configuration used to resolve the data for universe selection
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param universeSelector: Returns the symbols that should be included in the universe
        """
        ...

    @typing.overload
    def __init__(self, configuration: QuantConnect.Data.SubscriptionDataConfig, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, universeSelector: typing.Any) -> None:
        """
        Initializes a new instance of the FuncUniverse class
        
        :param configuration: The configuration used to resolve the data for universe selection
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param universeSelector: Returns the symbols that should be included in the universe
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs an initial, coarse filter
        
        :param utcTime: The current utc time
        :param data: The coarse fundamental data
        :returns: The data that passes the filter.
        """
        ...


class UniverseDecorator(QuantConnect.Data.UniverseSelection.Universe, metaclass=abc.ABCMeta):
    """
    Provides an implementation of UniverseSelection.Universe that redirects all calls to a
    wrapped (or decorated) universe. This provides scaffolding for other decorators who
    only need to override one or two methods.
    """

    @property
    def Universe(self) -> QuantConnect.Data.UniverseSelection.Universe:
        """
        The decorated universe instance
        
        This field is protected.
        """
        ...

    @property
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the settings used for subscriptions added for this universe"""
        ...

    @property
    def Securities(self) -> System.Collections.Concurrent.ConcurrentDictionary[QuantConnect.Symbol, QuantConnect.Data.UniverseSelection.Universe.Member]:
        """Gets the internal security collection used to define membership in this universe"""
        ...

    @Securities.setter
    def Securities(self, value: System.Collections.Concurrent.ConcurrentDictionary[QuantConnect.Symbol, QuantConnect.Data.UniverseSelection.Universe.Member]):
        """Gets the internal security collection used to define membership in this universe"""
        ...

    def __init__(self, universe: QuantConnect.Data.UniverseSelection.Universe) -> None:
        """
        Initializes a new instance of the UniverseDecorator class
        
        This method is protected.
        
        :param universe: The decorated universe. All overridable methods delegate to this instance.
        """
        ...

    def CanRemoveMember(self, utcTime: typing.Union[datetime.datetime, datetime.date], security: QuantConnect.Securities.Security) -> bool:
        """
        Determines whether or not the specified security can be removed from
        this universe. This is useful to prevent securities from being taken
        out of a universe before the algorithm has had enough time to make
        decisions on the security
        
        :param utcTime: The current utc time
        :param security: The security to check if its ok to remove
        :returns: True if we can remove the security, false otherwise.
        """
        ...

    def CreateSecurity(self, symbol: typing.Union[QuantConnect.Symbol, str], algorithm: QuantConnect.Interfaces.IAlgorithm, marketHoursDatabase: QuantConnect.Securities.MarketHoursDatabase, symbolPropertiesDatabase: QuantConnect.Securities.SymbolPropertiesDatabase) -> QuantConnect.Securities.Security:
        """
        Creates and configures a security for the specified symbol
        
        CreateSecurity is obsolete and will not be called. The system will create the required Securities based on selected symbols
        
        :param symbol: The symbol of the security to be created
        :param algorithm: The algorithm instance
        :param marketHoursDatabase: The market hours database
        :param symbolPropertiesDatabase: The symbol properties database
        :returns: The newly initialized security object.
        """
        warnings.warn("CreateSecurity is obsolete and will not be called. The system will create the required Securities based on selected symbols", DeprecationWarning)

    @typing.overload
    def GetSubscriptionRequests(self, security: QuantConnect.Securities.Security, currentTimeUtc: typing.Union[datetime.datetime, datetime.date], maximumEndTimeUtc: typing.Union[datetime.datetime, datetime.date], subscriptionService: QuantConnect.Interfaces.ISubscriptionDataConfigService) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]:
        """
        Gets the subscription requests to be added for the specified security
        
        :param security: The security to get subscriptions for
        :param currentTimeUtc: The current time in utc. This is the frontier time of the algorithm
        :param maximumEndTimeUtc: The max end time
        :param subscriptionService: Instance which implements ISubscriptionDataConfigService interface
        :returns: All subscriptions required by this security.
        """
        ...

    @typing.overload
    def GetSubscriptionRequests(self, security: QuantConnect.Securities.Security, currentTimeUtc: typing.Union[datetime.datetime, datetime.date], maximumEndTimeUtc: typing.Union[datetime.datetime, datetime.date]) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]:
        """
        Gets the subscription requests to be added for the specified security
        
        This overload is obsolete and will not be called. It was not capable of creating new SubscriptionDataConfig due to lack of information
        
        :param security: The security to get subscriptions for
        :param currentTimeUtc: The current time in utc. This is the frontier time of the algorithm
        :param maximumEndTimeUtc: The max end time
        :returns: All subscriptions required by this security.
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs universe selection using the data specified
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...


class GetSubscriptionRequestsUniverseDecorator(QuantConnect.Data.UniverseSelection.UniverseDecorator):
    """Provides a universe decoration that replaces the implementation of GetSubscriptionRequests"""

    def __init__(self, universe: QuantConnect.Data.UniverseSelection.Universe, getRequests: typing.Callable[[QuantConnect.Securities.Security, datetime.datetime, datetime.datetime], System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]]) -> None:
        """
        Initializes a new instance of the GetSubscriptionRequestsUniverseDecorator class
        
        :param universe: The universe to be decorated
        """
        ...

    def GetSubscriptionRequests(self, security: QuantConnect.Securities.Security, currentTimeUtc: typing.Union[datetime.datetime, datetime.date], maximumEndTimeUtc: typing.Union[datetime.datetime, datetime.date]) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]:
        """
        Gets the subscription requests to be added for the specified security
        
        :param security: The security to get subscriptions for
        :param currentTimeUtc: The current time in utc. This is the frontier time of the algorithm
        :param maximumEndTimeUtc: The max end time
        :returns: All subscriptions required by this security.
        """
        ...

    def GetSubscriptionRequestsDelegate(self, security: QuantConnect.Securities.Security, currentTimeUtc: typing.Union[datetime.datetime, datetime.date], maximumEndTimeUtc: typing.Union[datetime.datetime, datetime.date]) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]:
        """
        Delegate type for the GetSubscriptionRequests method
        
        :param security: The security to get subscription requests for
        :param currentTimeUtc: The current utc frontier time
        :returns: The subscription requests for the security to be given to the data feed.
        """
        ...


class ConstituentsUniverseData(QuantConnect.Data.BaseData):
    """Custom base data class used for ConstituentsUniverse"""

    @property
    def EndTime(self) -> datetime.datetime:
        """The end time of this data."""
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """The end time of this data."""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the CoarseFundamental class"""
        ...

    def DefaultResolution(self) -> int:
        """
        Gets the default resolution for this data and security type
        
        :returns: This method returns the int value of a member of the QuantConnect.Resolution enum.
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the URL string source of the file. This will be converted to a stream
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: String URL of source file.
        """
        ...

    def IsSparseData(self) -> bool:
        """
        Indicates that the data set is expected to be sparse
        
        :returns: True if the data set represented by this type is expected to be sparse.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects. Each data type creates its own factory method, and returns a new instance of the object
        each time it is called.
        
        :param config: Subscription data config setup object
        :param line: Line of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Instance of the T:BaseData object generated by this line of the CSV.
        """
        ...

    def RequiresMapping(self) -> bool:
        """
        Indicates if there is support for mapping
        
        :returns: True indicates mapping should be used.
        """
        ...

    def SupportedResolutions(self) -> System.Collections.Generic.List[QuantConnect.Resolution]:
        """Gets the supported resolution for this data and security type"""
        ...


class ConstituentsUniverse(typing.Generic[QuantConnect_Data_UniverseSelection_ConstituentsUniverse_T], QuantConnect.Data.UniverseSelection.FuncUniverse[QuantConnect_Data_UniverseSelection_ConstituentsUniverse_T]):
    """
    ConstituentsUniverse allows to perform universe selection based on an
    already preselected set of Symbol.
    """

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, constituentsFilter: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect_Data_UniverseSelection_ConstituentsUniverse_T]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]] = None) -> None:
        """
        Creates a new instance of the ConstituentsUniverse
        
        :param symbol: The universe symbol
        :param universeSettings: The universe settings to use
        :param constituentsFilter: User-provided function to filter constituents universe with
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, constituentsFilter: typing.Any = None) -> None:
        """
        Creates a new instance of the ConstituentsUniverse
        
        :param symbol: The universe symbol
        :param universeSettings: The universe settings to use
        :param constituentsFilter: User-provided function to filter constituents universe with
        """
        ...

    @typing.overload
    def __init__(self, subscriptionDataConfig: QuantConnect.Data.SubscriptionDataConfig, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, constituentsFilter: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect_Data_UniverseSelection_ConstituentsUniverse_T]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]] = None) -> None:
        """
        Creates a new instance of the ConstituentsUniverse
        
        :param subscriptionDataConfig: The universe configuration to use
        :param universeSettings: The universe settings to use
        :param constituentsFilter: User-provided function to filter constituents universe with
        """
        ...

    @typing.overload
    def __init__(self, subscriptionDataConfig: QuantConnect.Data.SubscriptionDataConfig, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, constituentsFilter: typing.Any = None) -> None:
        """
        Constituent universe for a Python function
        
        :param subscriptionDataConfig: The universe configuration to use
        :param universeSettings: The universe settings to use
        :param constituentsFilter: User-provided function to filter constituents universe with
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, filterFunc: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.ConstituentsUniverseData]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]]) -> None:
        """
        Creates a new instance of the ConstituentsUniverse
        
        :param symbol: The universe symbol
        :param universeSettings: The universe settings to use
        :param filterFunc: The constituents filter function
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings) -> None:
        """
        Creates a new instance of the ConstituentsUniverse
        
        :param symbol: The universe symbol
        :param universeSettings: The universe settings to use
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, filterFunc: typing.Any) -> None:
        """
        Creates a new instance of the ConstituentsUniverse
        
        :param symbol: The universe symbol
        :param universeSettings: The universe settings to use
        :param filterFunc: The constituents filter function
        """
        ...


class UniverseExtensions(System.Object):
    """Provides extension methods for the Universe class"""

    @staticmethod
    def ChainedTo(first: QuantConnect.Data.UniverseSelection.Universe, second: QuantConnect.Data.UniverseSelection.Universe, configurationPerSymbol: bool) -> QuantConnect.Data.UniverseSelection.Universe:
        """
        Creates a new universe that logically is the result of wiring the two universes together such that
        the first will produce subscriptions for the second and the second will only select on data that has
        passed the first.
        
        NOTE: The  and  universe instances provided
        to this method should not be manually added to the algorithm.
        
        :param first: The first universe in this 'chain'
        :param second: The second universe in this 'chain'
        :param configurationPerSymbol: True if each symbol as its own configuration, false otherwise
        :returns: A new universe that can be added to the algorithm that represents invoking the first universe and then the second universe using the outputs of the first.
        """
        ...

    @staticmethod
    def PrefilterUsing(second: QuantConnect.Data.UniverseSelection.Universe, first: QuantConnect.Data.UniverseSelection.Universe) -> QuantConnect.Data.UniverseSelection.Universe:
        """
        Creates a new universe that restricts the universe selection data to symbols that passed the
        first universe's selection critera
        
        NOTE: The  universe instance provided to this method should not be manually
        added to the algorithm. The  should still be manually (assuming no other changes).
        
        :param second: The universe to be filtere
        :param first: The universe providing the set of symbols used for filtered
        :returns: A new universe that can be added to the algorithm that represents invoking the second using the selections from the first as a filter.
        """
        ...


class CoarseFundamental(QuantConnect.Data.BaseData):
    """Defines summary information about a single symbol for a given date"""

    @property
    def Market(self) -> str:
        """Gets the market for this symbol"""
        ...

    @Market.setter
    def Market(self, value: str):
        """Gets the market for this symbol"""
        ...

    @property
    def DollarVolume(self) -> float:
        """Gets the day's dollar volume for this symbol"""
        ...

    @DollarVolume.setter
    def DollarVolume(self, value: float):
        """Gets the day's dollar volume for this symbol"""
        ...

    @property
    def Volume(self) -> int:
        """Gets the day's total volume"""
        ...

    @Volume.setter
    def Volume(self, value: int):
        """Gets the day's total volume"""
        ...

    @property
    def HasFundamentalData(self) -> bool:
        """Returns whether the symbol has fundamental data for the given date"""
        ...

    @HasFundamentalData.setter
    def HasFundamentalData(self, value: bool):
        """Returns whether the symbol has fundamental data for the given date"""
        ...

    @property
    def PriceFactor(self) -> float:
        """Gets the price factor for the given date"""
        ...

    @PriceFactor.setter
    def PriceFactor(self, value: float):
        """Gets the price factor for the given date"""
        ...

    @property
    def SplitFactor(self) -> float:
        """Gets the split factor for the given date"""
        ...

    @SplitFactor.setter
    def SplitFactor(self, value: float):
        """Gets the split factor for the given date"""
        ...

    @property
    def PriceScaleFactor(self) -> float:
        """Gets the combined factor used to create adjusted prices from raw prices"""
        ...

    @property
    def AdjustedPrice(self) -> float:
        """Gets the split and dividend adjusted price"""
        ...

    @property
    def EndTime(self) -> datetime.datetime:
        """The end time of this data."""
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """The end time of this data."""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the CoarseFundamental class"""
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Return a new instance clone of this object, used in fill forward
        
        :returns: A clone of the current object.
        """
        ...

    @staticmethod
    def CreateUniverseSymbol(market: str) -> QuantConnect.Symbol:
        """
        Creates the symbol used for coarse fundamental data
        
        :param market: The market
        :returns: A coarse universe symbol for the specified market.
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the URL string source of the file. This will be converted to a stream
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: String URL of source file.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects. Each data type creates its own factory method, and returns a new instance of the object
        each time it is called.
        
        :param config: Subscription data config setup object
        :param line: Line of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Instance of the T:BaseData object generated by this line of the CSV.
        """
        ...

    @staticmethod
    def ToRow(coarse: QuantConnect.Data.UniverseSelection.CoarseFundamental) -> str:
        """Converts a given fundamental data point into row format"""
        ...


class OptionChainUniverseDataCollection(QuantConnect.Data.UniverseSelection.BaseDataCollection):
    """Defines the universe selection data type for OptionChainUniverse"""

    @property
    def Underlying(self) -> QuantConnect.Data.BaseData:
        """The option chain's underlying price data"""
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Data.BaseData):
        """The option chain's underlying price data"""
        ...

    @property
    def FilteredContracts(self) -> System.Collections.Generic.HashSet[QuantConnect.Symbol]:
        """Gets or sets the contracts selected by the universe"""
        ...

    @FilteredContracts.setter
    def FilteredContracts(self, value: System.Collections.Generic.HashSet[QuantConnect.Symbol]):
        """Gets or sets the contracts selected by the universe"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Initializes a new default instance of the OptionChainUniverseDataCollection c;ass"""
        ...

    @typing.overload
    def __init__(self, time: typing.Union[datetime.datetime, datetime.date], symbol: typing.Union[QuantConnect.Symbol, str], data: System.Collections.Generic.List[QuantConnect.Data.BaseData] = None, underlying: QuantConnect.Data.BaseData = None) -> None:
        """
        Initializes a new instance of the OptionChainUniverseDataCollection class
        
        :param time: The time of this data
        :param symbol: A common identifier for all data in this packet
        :param data: The data to add to this collection
        :param underlying: The option chain's underlying price data
        """
        ...

    @typing.overload
    def __init__(self, time: typing.Union[datetime.datetime, datetime.date], endTime: typing.Union[datetime.datetime, datetime.date], symbol: typing.Union[QuantConnect.Symbol, str], data: System.Collections.Generic.List[QuantConnect.Data.BaseData] = None, underlying: QuantConnect.Data.BaseData = None) -> None:
        """
        Initializes a new instance of the OptionChainUniverseDataCollection class
        
        :param time: The start time of this data
        :param endTime: The end time of this data
        :param symbol: A common identifier for all data in this packet
        :param data: The data to add to this collection
        :param underlying: The option chain's underlying price data
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Return a new instance clone of this object, used in fill forward
        
        :returns: A clone of the current object.
        """
        ...


class UniversePythonWrapper(QuantConnect.Data.UniverseSelection.Universe):
    """Provides an implementation of Universe that wraps a PyObject object"""

    @property
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the settings used for subscriptions added for this universe"""
        ...

    @property
    def DisposeRequested(self) -> bool:
        """Flag indicating if disposal of this universe has been requested"""
        ...

    @DisposeRequested.setter
    def DisposeRequested(self, value: bool):
        """Flag indicating if disposal of this universe has been requested"""
        ...

    @property
    def Configuration(self) -> QuantConnect.Data.SubscriptionDataConfig:
        """Gets the configuration used to get universe data"""
        ...

    @Configuration.setter
    def Configuration(self, value: QuantConnect.Data.SubscriptionDataConfig):
        """Gets the configuration used to get universe data"""
        ...

    @property
    def Securities(self) -> System.Collections.Concurrent.ConcurrentDictionary[QuantConnect.Symbol, QuantConnect.Data.UniverseSelection.Universe.Member]:
        """Gets the internal security collection used to define membership in this universe"""
        ...

    @Securities.setter
    def Securities(self, value: System.Collections.Concurrent.ConcurrentDictionary[QuantConnect.Symbol, QuantConnect.Data.UniverseSelection.Universe.Member]):
        """Gets the internal security collection used to define membership in this universe"""
        ...

    def __init__(self, universe: typing.Any) -> None:
        """Initializes a new instance of the UniversePythonWrapper class"""
        ...

    def GetSubscriptionRequests(self, security: QuantConnect.Securities.Security, currentTimeUtc: typing.Union[datetime.datetime, datetime.date], maximumEndTimeUtc: typing.Union[datetime.datetime, datetime.date], subscriptionService: QuantConnect.Interfaces.ISubscriptionDataConfigService) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]:
        """
        Gets the subscription requests to be added for the specified security
        
        :param security: The security to get subscriptions for
        :param currentTimeUtc: The current time in utc. This is the frontier time of the algorithm
        :param maximumEndTimeUtc: The max end time
        :param subscriptionService: Instance which implements ISubscriptionDataConfigService interface
        :returns: All subscriptions required by this security.
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs universe selection using the data specified
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...


class FuturesChainUniverseDataCollection(QuantConnect.Data.UniverseSelection.BaseDataCollection):
    """Defines the universe selection data type for FuturesChainUniverse"""

    @property
    def FilteredContracts(self) -> System.Collections.Generic.HashSet[QuantConnect.Symbol]:
        """Gets or sets the contracts selected by the universe"""
        ...

    @FilteredContracts.setter
    def FilteredContracts(self, value: System.Collections.Generic.HashSet[QuantConnect.Symbol]):
        """Gets or sets the contracts selected by the universe"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Initializes a new default instance of the FuturesChainUniverseDataCollection c;ass"""
        ...

    @typing.overload
    def __init__(self, time: typing.Union[datetime.datetime, datetime.date], symbol: typing.Union[QuantConnect.Symbol, str], data: System.Collections.Generic.List[QuantConnect.Data.BaseData] = None) -> None:
        """
        Initializes a new instance of the FuturesChainUniverseDataCollection class
        
        :param time: The time of this data
        :param symbol: A common identifier for all data in this packet
        :param data: The data to add to this collection
        """
        ...

    @typing.overload
    def __init__(self, time: typing.Union[datetime.datetime, datetime.date], endTime: typing.Union[datetime.datetime, datetime.date], symbol: typing.Union[QuantConnect.Symbol, str], data: System.Collections.Generic.List[QuantConnect.Data.BaseData] = None) -> None:
        """
        Initializes a new instance of the FuturesChainUniverseDataCollection class
        
        :param time: The start time of this data
        :param endTime: The end time of this data
        :param symbol: A common identifier for all data in this packet
        :param data: The data to add to this collection
        """
        ...

    def Clone(self) -> QuantConnect.Data.BaseData:
        """
        Return a new instance clone of this object, used in fill forward
        
        :returns: A clone of the current object.
        """
        ...


class FineFundamentalUniverse(QuantConnect.Data.UniverseSelection.Universe):
    """Defines a universe that reads fine us equity data"""

    @property
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the settings used for subscriptons added for this universe"""
        ...

    @typing.overload
    def __init__(self, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, selector: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect.Data.Fundamental.FineFundamental]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]]) -> None:
        """
        Initializes a new instance of the FineFundamentalUniverse class
        
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param selector: Returns the symbols that should be included in the universe
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, selector: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect.Data.Fundamental.FineFundamental]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]]) -> None:
        """
        Initializes a new instance of the FineFundamentalUniverse class
        
        :param symbol: Defines the symbol to use for this universe
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param selector: Returns the symbols that should be included in the universe
        """
        ...

    @staticmethod
    def CreateConfiguration(symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect.Data.SubscriptionDataConfig:
        """
        Creates a FineFundamental subscription configuration for the US-equity market
        
        :param symbol: The symbol used in the returned configuration
        :returns: A fine fundamental subscription configuration with the specified symbol.
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs universe selection using the data specified
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...


class SelectSymbolsUniverseDecorator(QuantConnect.Data.UniverseSelection.UniverseDecorator):
    """Provides a univese decoration that replaces the implementation of SelectSymbols"""

    def __init__(self, universe: QuantConnect.Data.UniverseSelection.Universe, selectSymbols: typing.Callable[[datetime.datetime, QuantConnect.Data.UniverseSelection.BaseDataCollection], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]]) -> None:
        """
        Initializes a new instance of the SelectSymbolsUniverseDecorator class
        
        :param universe: The universe to be decorated
        :param selectSymbols: The new implementation of SelectSymbols
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs universe selection using the data specified
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...

    def SelectSymbolsDelegate(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Delegate type for the SelectSymbols method
        
        :param utcTime: The current utc frontier time
        :param data: The universe selection data
        :returns: The symbols selected by the universe.
        """
        ...


class SecurityChanges(System.Object):
    """Defines the additions and subtractions to the algorithm's security subscriptions"""

    # Cannot convert to Python: None: QuantConnect.Data.UniverseSelection.SecurityChanges = ...
    """Gets an instance that represents no changes have been made"""

    @property
    def Count(self) -> int:
        """Gets the total count of added and removed securities"""
        ...

    @property
    def FilterCustomSecurities(self) -> bool:
        """
        True will filter out custom securities from the
        AddedSecurities and RemovedSecurities properties
        """
        ...

    @FilterCustomSecurities.setter
    def FilterCustomSecurities(self, value: bool):
        """
        True will filter out custom securities from the
        AddedSecurities and RemovedSecurities properties
        """
        ...

    @property
    def AddedSecurities(self) -> System.Collections.Generic.IReadOnlyList[QuantConnect.Securities.Security]:
        """Gets the symbols that were added by universe selection"""
        ...

    @property
    def RemovedSecurities(self) -> System.Collections.Generic.IReadOnlyList[QuantConnect.Securities.Security]:
        """
        Gets the symbols that were removed by universe selection. This list may
        include symbols that were removed, but are still receiving data due to
        existing holdings or open orders
        """
        ...

    @typing.overload
    def __init__(self, addedSecurities: System.Collections.Generic.IEnumerable[QuantConnect.Securities.Security], removedSecurities: System.Collections.Generic.IEnumerable[QuantConnect.Securities.Security]) -> None:
        """
        Initializes a new instance of the SecurityChanges class
        
        :param addedSecurities: Added symbols list
        :param removedSecurities: Removed symbols list
        """
        ...

    @typing.overload
    def __init__(self, changes: QuantConnect.Data.UniverseSelection.SecurityChanges) -> None:
        """
        Initializes a new instance of the SecurityChanges class
        as a shallow clone of a given instance, sharing the same collections
        
        :param changes: The instance to clone
        """
        ...

    @staticmethod
    def Added(*securities: QuantConnect.Securities.Security) -> QuantConnect.Data.UniverseSelection.SecurityChanges:
        """
        Returns a new instance of SecurityChanges with the specified securities marked as added
        
        :param securities: The added securities
        :returns: A new security changes instance with the specified securities marked as added.
        """
        ...

    @staticmethod
    def Removed(*securities: QuantConnect.Securities.Security) -> QuantConnect.Data.UniverseSelection.SecurityChanges:
        """
        Returns a new instance of SecurityChanges with the specified securities marked as removed
        
        :param securities: The removed securities
        :returns: A new security changes instance with the specified securities marked as removed.
        """
        ...

    def ToString(self) -> str:
        ...


class CoarseFundamentalUniverse(QuantConnect.Data.UniverseSelection.Universe):
    """Defines a universe that reads coarse us equity data"""

    @property
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the settings used for subscriptons added for this universe"""
        ...

    @typing.overload
    def __init__(self, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, selector: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.CoarseFundamental]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]]) -> None:
        """
        Initializes a new instance of the CoarseFundamentalUniverse class
        
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param selector: Returns the symbols that should be included in the universe
        """
        ...

    @typing.overload
    def __init__(self, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, selector: typing.Any) -> None:
        """
        Initializes a new instance of the CoarseFundamentalUniverse class
        
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param selector: Returns the symbols that should be included in the universe
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, selector: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.CoarseFundamental]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]]) -> None:
        """
        Initializes a new instance of the CoarseFundamentalUniverse class
        
        :param symbol: Defines the symbol to use for this universe
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param selector: Returns the symbols that should be included in the universe
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, selector: typing.Any) -> None:
        """
        Initializes a new instance of the CoarseFundamentalUniverse class
        
        :param symbol: Defines the symbol to use for this universe
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param selector: Returns the symbols that should be included in the universe
        """
        ...

    @staticmethod
    def CreateConfiguration(symbol: typing.Union[QuantConnect.Symbol, str]) -> QuantConnect.Data.SubscriptionDataConfig:
        """
        Creates a CoarseFundamental subscription configuration for the US-equity market
        
        :param symbol: The symbol used in the returned configuration
        :returns: A coarse fundamental subscription configuration with the specified symbol.
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Performs universe selection using the data specified
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...


class FineFundamentalFilteredUniverse(QuantConnect.Data.UniverseSelection.SelectSymbolsUniverseDecorator):
    """Provides a universe that can be filtered with a FineFundamental selection function"""

    @property
    def FineFundamentalUniverse(self) -> QuantConnect.Data.UniverseSelection.FineFundamentalUniverse:
        """The universe that will be used for fine universe selection"""
        ...

    @FineFundamentalUniverse.setter
    def FineFundamentalUniverse(self, value: QuantConnect.Data.UniverseSelection.FineFundamentalUniverse):
        """The universe that will be used for fine universe selection"""
        ...

    @typing.overload
    def __init__(self, universe: QuantConnect.Data.UniverseSelection.Universe, fineSelector: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect.Data.Fundamental.FineFundamental]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]]) -> None:
        """
        Initializes a new instance of the FineFundamentalFilteredUniverse class
        
        :param universe: The universe to be filtered
        :param fineSelector: The fine selection function
        """
        ...

    @typing.overload
    def __init__(self, universe: QuantConnect.Data.UniverseSelection.Universe, fineSelector: typing.Any) -> None:
        """
        Initializes a new instance of the FineFundamentalFilteredUniverse class
        
        :param universe: The universe to be filtered
        :param fineSelector: The fine selection function
        """
        ...


class ETFConstituentsUniverse(QuantConnect.Data.UniverseSelection.ConstituentsUniverse[QuantConnect.Data.UniverseSelection.ETFConstituentData]):
    """Creates a universe based on an ETF's holdings at a given date"""

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, constituentsFilter: typing.Callable[[System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.ETFConstituentData]], System.Collections.Generic.IEnumerable[QuantConnect.Symbol]] = None) -> None:
        """
        Creates a new universe for the constituents of the ETF provided as
        
        :param symbol: The ETF to load constituents for
        :param universeSettings: Universe settings
        :param constituentsFilter: The filter function used to filter out ETF constituents from the universe
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, constituentsFilter: typing.Any = None) -> None:
        """
        Creates a new universe for the constituents of the ETF provided as
        
        :param symbol: The ETF to load constituents for
        :param universeSettings: Universe settings
        :param constituentsFilter: The filter function used to filter out ETF constituents from the universe
        """
        ...


class UserDefinedUniverse(QuantConnect.Data.UniverseSelection.Universe, System.Collections.Specialized.INotifyCollectionChanged, QuantConnect.Data.UniverseSelection.ITimeTriggeredUniverse):
    """
    Represents the universe defined by the user's algorithm. This is
    the default universe where manually added securities live by
    market/security type. They can also be manually generated and
    can be configured to fire on certain interval and will always
    return the internal list of symbols.
    """

    @property
    def CollectionChanged(self) -> _EventContainer[typing.Callable[[System.Object, System.Collections.Specialized.NotifyCollectionChangedEventArgs], None], None]:
        """Event fired when a symbol is added or removed from this universe"""
        ...

    @CollectionChanged.setter
    def CollectionChanged(self, value: _EventContainer[typing.Callable[[System.Object, System.Collections.Specialized.NotifyCollectionChangedEventArgs], None], None]):
        """Event fired when a symbol is added or removed from this universe"""
        ...

    @property
    def Interval(self) -> datetime.timedelta:
        """Gets the interval of this user defined universe"""
        ...

    @property
    def UniverseSettings(self) -> QuantConnect.Data.UniverseSelection.UniverseSettings:
        """Gets the settings used for subscriptons added for this universe"""
        ...

    @typing.overload
    def __init__(self, configuration: QuantConnect.Data.SubscriptionDataConfig, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, interval: datetime.timedelta, symbols: System.Collections.Generic.IEnumerable[QuantConnect.Symbol]) -> None:
        """
        Initializes a new instance of the UserDefinedUniverse class
        
        :param configuration: The configuration used to resolve the data for universe selection
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param interval: The interval at which selection should be performed
        :param symbols: The initial set of symbols in this universe
        """
        ...

    @typing.overload
    def __init__(self, configuration: QuantConnect.Data.SubscriptionDataConfig, universeSettings: QuantConnect.Data.UniverseSelection.UniverseSettings, interval: datetime.timedelta, selector: typing.Callable[[datetime.datetime], System.Collections.Generic.IEnumerable[str]]) -> None:
        """
        Initializes a new instance of the UserDefinedUniverse class
        
        :param configuration: The configuration used to resolve the data for universe selection
        :param universeSettings: The settings used for new subscriptions generated by this universe
        :param interval: The interval at which selection should be performed
        :param selector: Universe selection function invoked for each time returned via GetTriggerTimes. The function parameter is a DateTime in the time zone of configuration.ExchangeTimeZone
        """
        ...

    @typing.overload
    def Add(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Adds the specified Symbol to this universe
        
        :param symbol: The symbol to be added to this universe
        :returns: True if the symbol was added, false if it was already present.
        """
        ...

    @typing.overload
    def Add(self, subscriptionDataConfig: QuantConnect.Data.SubscriptionDataConfig) -> bool:
        """
        Adds the specified SubscriptionDataConfig to this universe
        
        :param subscriptionDataConfig: The subscription data configuration to be added to this universe
        :returns: True if the subscriptionDataConfig was added, false if it was already present.
        """
        ...

    @staticmethod
    def CreateSymbol(securityType: QuantConnect.SecurityType, market: str) -> QuantConnect.Symbol:
        """
        Creates a user defined universe symbol
        
        :param securityType: The security
        :param market: The market
        :returns: A symbol for user defined universe of the specified security type and market.
        """
        ...

    def GetSubscriptionRequests(self, security: QuantConnect.Securities.Security, currentTimeUtc: typing.Union[datetime.datetime, datetime.date], maximumEndTimeUtc: typing.Union[datetime.datetime, datetime.date], subscriptionService: QuantConnect.Interfaces.ISubscriptionDataConfigService) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.UniverseSelection.SubscriptionRequest]:
        """
        Gets the subscription requests to be added for the specified security
        
        :param security: The security to get subscriptions for
        :param currentTimeUtc: The current time in utc. This is the frontier time of the algorithm
        :param maximumEndTimeUtc: The max end time
        :param subscriptionService: Instance which implements ISubscriptionDataConfigService interface
        :returns: All subscriptions required by this security.
        """
        ...

    def GetTriggerTimes(self, startTimeUtc: typing.Union[datetime.datetime, datetime.date], endTimeUtc: typing.Union[datetime.datetime, datetime.date], marketHoursDatabase: QuantConnect.Securities.MarketHoursDatabase) -> System.Collections.Generic.IEnumerable[datetime.datetime]:
        """
        Returns an enumerator that defines when this user defined universe will be invoked
        
        :returns: An enumerator of DateTime that defines when this universe will be invoked.
        """
        ...

    def OnCollectionChanged(self, e: System.Collections.Specialized.NotifyCollectionChangedEventArgs) -> None:
        """
        Event invocator for the CollectionChanged event
        
        This method is protected.
        
        :param e: The notify collection changed event arguments
        """
        ...

    def Remove(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Removes the specified Symbol from this universe
        
        :param symbol: The symbol to be removed
        :returns: True if the symbol was removed, false if the symbol was not present.
        """
        ...

    def SelectSymbols(self, utcTime: typing.Union[datetime.datetime, datetime.date], data: QuantConnect.Data.UniverseSelection.BaseDataCollection) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Returns the symbols defined by the user for this universe
        
        :param utcTime: The current utc time
        :param data: The symbols to remain in the universe
        :returns: The data that passes the filter.
        """
        ...


class _EventContainer(typing.Generic[QuantConnect_Data_UniverseSelection__EventContainer_Callable, QuantConnect_Data_UniverseSelection__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Data_UniverseSelection__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Data_UniverseSelection__EventContainer_Callable) -> None:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Data_UniverseSelection__EventContainer_Callable) -> None:
        """Unregisters an event handler."""
        ...


