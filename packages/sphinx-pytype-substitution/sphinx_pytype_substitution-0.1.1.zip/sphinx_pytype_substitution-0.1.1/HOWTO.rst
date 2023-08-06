
First add the :code:`sphinx_pytype_substitution` to the extensions list
in :code:`config.py`.

.. code-block:: python

    # Add any Sphinx extension module names here, as strings. They can be
    # extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
    # ones.
    extensions = [
        'sphinx_pytype_substitution',
        'sphinx_rtd_theme',
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.doctest',
        'sphinx.ext.mathjax',
        'sphinx.ext.viewcode',
        'sphinx.ext.napoleon'
    ]

Then set the module to reference (here :code:`datetime`)
by appending it the following in :code:`config.py`

.. code-block:: python

    # -- Config for pytype_substitution extension ------------------------------

    pytype_substitutions = datetime,  # package, module or class to reference to

This will generate and add something like (full list follows below)

.. code-block:: rst

    .. |datetime|                                     replace:: :py:mod:`datetime`
    .. |datetime.MAXYEAR|                             replace:: :py:const:`datetime.MAXYEAR`
    .. |datetime.MINYEAR|                             replace:: :py:const:`datetime.MINYEAR`
    .. |datetime.date|                                replace:: :py:class:`datetime.date`
    .. |datetime.date()|                              replace:: :py:class:`datetime.date`
    .. |datetime.date().day|                          replace:: :py:attr:`datetime.date.day`
    .. |datetime.date().max|                          replace:: :py:attr:`datetime.date.max`
    .. |datetime.date().min|                          replace:: :py:attr:`datetime.date.min`
    .. |datetime.date().month|                        replace:: :py:attr:`datetime.date.month`
    .. |datetime.date().resolution|                   replace:: :py:attr:`datetime.date.resolution`
    .. |datetime.date().year|                         replace:: :py:attr:`datetime.date.year`
    .. |datetime.date().timetuple()|                  replace:: :py:func:`datetime.date.timetuple`
    .. |datetime.date().today()|                      replace:: :py:func:`datetime.date.today`
    .. |datetime.date().toordinal()|                  replace:: :py:func:`datetime.date.toordinal`
    .. |datetime.date().weekday()|                    replace:: :py:func:`datetime.date.weekday`

and more...

But

.. code-block:: python

    # -- Config for pytype_substitution extension ------------------------------

    pytype_substitutions = datetime,  # package, module or class to reference to
    pytype_short_ref = True  # drop module from reference (if it does not conflict)

will generate and add something like

.. code-block:: rst

    .. |datetime|                                     replace:: :py:mod:`datetime`
    .. |MAXYEAR|                             replace:: :py:const:`datetime.MAXYEAR`
    .. |MINYEAR|                             replace:: :py:const:`datetime.MINYEAR`
    .. |date|                                replace:: :py:class:`datetime.date`
    .. |date()|                              replace:: :py:class:`datetime.date`
    .. |date().day|                          replace:: :py:attr:`datetime.date.day`
    .. |date().max|                          replace:: :py:attr:`datetime.date.max`
    .. |date().min|                          replace:: :py:attr:`datetime.date.min`
    .. |date().month|                        replace:: :py:attr:`datetime.date.month`
    .. |date().resolution|                   replace:: :py:attr:`datetime.date.resolution`
    .. |date().year|                         replace:: :py:attr:`datetime.date.year`
    .. |date().timetuple()|                  replace:: :py:func:`datetime.date.timetuple`
    .. |date().today()|                      replace:: :py:func:`datetime.date.today`
    .. |date().toordinal()|                  replace:: :py:func:`datetime.date.toordinal`
    .. |date().weekday()|                    replace:: :py:func:`datetime.date.weekday`

Full :code:`datetime` reference substitutions
---------------------------------------------

.. code-block:: rst

    .. |datetime.date().day|                          replace:: :py:attr:`datetime.date.day`
    .. |datetime.date().max|                          replace:: :py:attr:`datetime.date.max`
    .. |datetime.date().min|                          replace:: :py:attr:`datetime.date.min`
    .. |datetime.date().month|                        replace:: :py:attr:`datetime.date.month`
    .. |datetime.date().resolution|                   replace:: :py:attr:`datetime.date.resolution`
    .. |datetime.date().year|                         replace:: :py:attr:`datetime.date.year`
    .. |datetime.datetime().day|                      replace:: :py:attr:`datetime.datetime.day`
    .. |datetime.datetime().fold|                     replace:: :py:attr:`datetime.datetime.fold`
    .. |datetime.datetime().hour|                     replace:: :py:attr:`datetime.datetime.hour`
    .. |datetime.datetime().max|                      replace:: :py:attr:`datetime.datetime.max`
    .. |datetime.datetime().microsecond|              replace:: :py:attr:`datetime.datetime.microsecond`
    .. |datetime.datetime().min|                      replace:: :py:attr:`datetime.datetime.min`
    .. |datetime.datetime().minute|                   replace:: :py:attr:`datetime.datetime.minute`
    .. |datetime.datetime().month|                    replace:: :py:attr:`datetime.datetime.month`
    .. |datetime.datetime().resolution|               replace:: :py:attr:`datetime.datetime.resolution`
    .. |datetime.datetime().second|                   replace:: :py:attr:`datetime.datetime.second`
    .. |datetime.datetime().tzinfo|                   replace:: :py:attr:`datetime.datetime.tzinfo`
    .. |datetime.datetime().year|                     replace:: :py:attr:`datetime.datetime.year`
    .. |datetime.datetime_CAPI|                       replace:: :py:attr:`datetime.datetime_CAPI`
    .. |datetime.time().fold|                         replace:: :py:attr:`datetime.time.fold`
    .. |datetime.time().hour|                         replace:: :py:attr:`datetime.time.hour`
    .. |datetime.time().max|                          replace:: :py:attr:`datetime.time.max`
    .. |datetime.time().microsecond|                  replace:: :py:attr:`datetime.time.microsecond`
    .. |datetime.time().min|                          replace:: :py:attr:`datetime.time.min`
    .. |datetime.time().minute|                       replace:: :py:attr:`datetime.time.minute`
    .. |datetime.time().resolution|                   replace:: :py:attr:`datetime.time.resolution`
    .. |datetime.time().second|                       replace:: :py:attr:`datetime.time.second`
    .. |datetime.time().tzinfo|                       replace:: :py:attr:`datetime.time.tzinfo`
    .. |datetime.timedelta().days|                    replace:: :py:attr:`datetime.timedelta.days`
    .. |datetime.timedelta().max|                     replace:: :py:attr:`datetime.timedelta.max`
    .. |datetime.timedelta().microseconds|            replace:: :py:attr:`datetime.timedelta.microseconds`
    .. |datetime.timedelta().min|                     replace:: :py:attr:`datetime.timedelta.min`
    .. |datetime.timedelta().resolution|              replace:: :py:attr:`datetime.timedelta.resolution`
    .. |datetime.timedelta().seconds|                 replace:: :py:attr:`datetime.timedelta.seconds`
    .. |datetime.timezone().max|                      replace:: :py:attr:`datetime.timezone.max`
    .. |datetime.timezone().min|                      replace:: :py:attr:`datetime.timezone.min`
    .. |datetime.timezone().utc|                      replace:: :py:attr:`datetime.timezone.utc`
    .. |datetime.date|                                replace:: :py:class:`datetime.date`
    .. |datetime.date()|                              replace:: :py:class:`datetime.date`
    .. |datetime.datetime|                            replace:: :py:class:`datetime.datetime`
    .. |datetime.datetime()|                          replace:: :py:class:`datetime.datetime`
    .. |datetime.time|                                replace:: :py:class:`datetime.time`
    .. |datetime.time()|                              replace:: :py:class:`datetime.time`
    .. |datetime.timedelta|                           replace:: :py:class:`datetime.timedelta`
    .. |datetime.timedelta()|                         replace:: :py:class:`datetime.timedelta`
    .. |datetime.timezone|                            replace:: :py:class:`datetime.timezone`
    .. |datetime.timezone()|                          replace:: :py:class:`datetime.timezone`
    .. |datetime.tzinfo|                              replace:: :py:class:`datetime.tzinfo`
    .. |datetime.tzinfo()|                            replace:: :py:class:`datetime.tzinfo`
    .. |datetime.MAXYEAR|                             replace:: :py:const:`datetime.MAXYEAR`
    .. |datetime.MINYEAR|                             replace:: :py:const:`datetime.MINYEAR`
    .. |datetime.date().ctime()|                      replace:: :py:func:`datetime.date.ctime`
    .. |datetime.date().fromisocalendar()|            replace:: :py:func:`datetime.date.fromisocalendar`
    .. |datetime.date().fromisoformat()|              replace:: :py:func:`datetime.date.fromisoformat`
    .. |datetime.date().fromordinal()|                replace:: :py:func:`datetime.date.fromordinal`
    .. |datetime.date().fromtimestamp()|              replace:: :py:func:`datetime.date.fromtimestamp`
    .. |datetime.date().isocalendar()|                replace:: :py:func:`datetime.date.isocalendar`
    .. |datetime.date().isoformat()|                  replace:: :py:func:`datetime.date.isoformat`
    .. |datetime.date().isoweekday()|                 replace:: :py:func:`datetime.date.isoweekday`
    .. |datetime.date().replace()|                    replace:: :py:func:`datetime.date.replace`
    .. |datetime.date().strftime()|                   replace:: :py:func:`datetime.date.strftime`
    .. |datetime.date().timetuple()|                  replace:: :py:func:`datetime.date.timetuple`
    .. |datetime.date().today()|                      replace:: :py:func:`datetime.date.today`
    .. |datetime.date().toordinal()|                  replace:: :py:func:`datetime.date.toordinal`
    .. |datetime.date().weekday()|                    replace:: :py:func:`datetime.date.weekday`
    .. |datetime.datetime().astimezone()|             replace:: :py:func:`datetime.datetime.astimezone`
    .. |datetime.datetime().combine()|                replace:: :py:func:`datetime.datetime.combine`
    .. |datetime.datetime().ctime()|                  replace:: :py:func:`datetime.datetime.ctime`
    .. |datetime.datetime().date()|                   replace:: :py:func:`datetime.datetime.date`
    .. |datetime.datetime().dst()|                    replace:: :py:func:`datetime.datetime.dst`
    .. |datetime.datetime().fromisocalendar()|        replace:: :py:func:`datetime.datetime.fromisocalendar`
    .. |datetime.datetime().fromisoformat()|          replace:: :py:func:`datetime.datetime.fromisoformat`
    .. |datetime.datetime().fromordinal()|            replace:: :py:func:`datetime.datetime.fromordinal`
    .. |datetime.datetime().fromtimestamp()|          replace:: :py:func:`datetime.datetime.fromtimestamp`
    .. |datetime.datetime().isocalendar()|            replace:: :py:func:`datetime.datetime.isocalendar`
    .. |datetime.datetime().isoformat()|              replace:: :py:func:`datetime.datetime.isoformat`
    .. |datetime.datetime().isoweekday()|             replace:: :py:func:`datetime.datetime.isoweekday`
    .. |datetime.datetime().now()|                    replace:: :py:func:`datetime.datetime.now`
    .. |datetime.datetime().replace()|                replace:: :py:func:`datetime.datetime.replace`
    .. |datetime.datetime().strftime()|               replace:: :py:func:`datetime.datetime.strftime`
    .. |datetime.datetime().strptime()|               replace:: :py:func:`datetime.datetime.strptime`
    .. |datetime.datetime().time()|                   replace:: :py:func:`datetime.datetime.time`
    .. |datetime.datetime().timestamp()|              replace:: :py:func:`datetime.datetime.timestamp`
    .. |datetime.datetime().timetuple()|              replace:: :py:func:`datetime.datetime.timetuple`
    .. |datetime.datetime().timetz()|                 replace:: :py:func:`datetime.datetime.timetz`
    .. |datetime.datetime().today()|                  replace:: :py:func:`datetime.datetime.today`
    .. |datetime.datetime().toordinal()|              replace:: :py:func:`datetime.datetime.toordinal`
    .. |datetime.datetime().tzname()|                 replace:: :py:func:`datetime.datetime.tzname`
    .. |datetime.datetime().utcfromtimestamp()|       replace:: :py:func:`datetime.datetime.utcfromtimestamp`
    .. |datetime.datetime().utcnow()|                 replace:: :py:func:`datetime.datetime.utcnow`
    .. |datetime.datetime().utcoffset()|              replace:: :py:func:`datetime.datetime.utcoffset`
    .. |datetime.datetime().utctimetuple()|           replace:: :py:func:`datetime.datetime.utctimetuple`
    .. |datetime.datetime().weekday()|                replace:: :py:func:`datetime.datetime.weekday`
    .. |datetime.time().dst()|                        replace:: :py:func:`datetime.time.dst`
    .. |datetime.time().fromisoformat()|              replace:: :py:func:`datetime.time.fromisoformat`
    .. |datetime.time().isoformat()|                  replace:: :py:func:`datetime.time.isoformat`
    .. |datetime.time().replace()|                    replace:: :py:func:`datetime.time.replace`
    .. |datetime.time().strftime()|                   replace:: :py:func:`datetime.time.strftime`
    .. |datetime.time().tzname()|                     replace:: :py:func:`datetime.time.tzname`
    .. |datetime.time().utcoffset()|                  replace:: :py:func:`datetime.time.utcoffset`
    .. |datetime.timedelta().total_seconds()|         replace:: :py:func:`datetime.timedelta.total_seconds`
    .. |datetime.timezone().dst()|                    replace:: :py:func:`datetime.timezone.dst`
    .. |datetime.timezone().fromutc()|                replace:: :py:func:`datetime.timezone.fromutc`
    .. |datetime.timezone().tzname()|                 replace:: :py:func:`datetime.timezone.tzname`
    .. |datetime.timezone().utcoffset()|              replace:: :py:func:`datetime.timezone.utcoffset`
    .. |datetime.tzinfo().dst()|                      replace:: :py:func:`datetime.tzinfo.dst`
    .. |datetime.tzinfo().fromutc()|                  replace:: :py:func:`datetime.tzinfo.fromutc`
    .. |datetime.tzinfo().tzname()|                   replace:: :py:func:`datetime.tzinfo.tzname`
    .. |datetime.tzinfo().utcoffset()|                replace:: :py:func:`datetime.tzinfo.utcoffset`
    .. |datetime|                                     replace:: :py:mod:`datetime`
    .. |datetime.date().day|                          replace:: :py:attr:`datetime.date.day`
    .. |datetime.date().max|                          replace:: :py:attr:`datetime.date.max`
    .. |datetime.date().min|                          replace:: :py:attr:`datetime.date.min`
    .. |datetime.date().month|                        replace:: :py:attr:`datetime.date.month`
    .. |datetime.date().resolution|                   replace:: :py:attr:`datetime.date.resolution`
    .. |datetime.date().year|                         replace:: :py:attr:`datetime.date.year`
    .. |datetime.datetime().day|                      replace:: :py:attr:`datetime.datetime.day`
    .. |datetime.datetime().fold|                     replace:: :py:attr:`datetime.datetime.fold`
    .. |datetime.datetime().hour|                     replace:: :py:attr:`datetime.datetime.hour`
    .. |datetime.datetime().max|                      replace:: :py:attr:`datetime.datetime.max`
    .. |datetime.datetime().microsecond|              replace:: :py:attr:`datetime.datetime.microsecond`
    .. |datetime.datetime().min|                      replace:: :py:attr:`datetime.datetime.min`
    .. |datetime.datetime().minute|                   replace:: :py:attr:`datetime.datetime.minute`
    .. |datetime.datetime().month|                    replace:: :py:attr:`datetime.datetime.month`
    .. |datetime.datetime().resolution|               replace:: :py:attr:`datetime.datetime.resolution`
    .. |datetime.datetime().second|                   replace:: :py:attr:`datetime.datetime.second`
    .. |datetime.datetime().tzinfo|                   replace:: :py:attr:`datetime.datetime.tzinfo`
    .. |datetime.datetime().year|                     replace:: :py:attr:`datetime.datetime.year`
    .. |datetime.datetime_CAPI|                       replace:: :py:attr:`datetime.datetime_CAPI`
    .. |datetime.time().fold|                         replace:: :py:attr:`datetime.time.fold`
    .. |datetime.time().hour|                         replace:: :py:attr:`datetime.time.hour`
    .. |datetime.time().max|                          replace:: :py:attr:`datetime.time.max`
    .. |datetime.time().microsecond|                  replace:: :py:attr:`datetime.time.microsecond`
    .. |datetime.time().min|                          replace:: :py:attr:`datetime.time.min`
    .. |datetime.time().minute|                       replace:: :py:attr:`datetime.time.minute`
    .. |datetime.time().resolution|                   replace:: :py:attr:`datetime.time.resolution`
    .. |datetime.time().second|                       replace:: :py:attr:`datetime.time.second`
    .. |datetime.time().tzinfo|                       replace:: :py:attr:`datetime.time.tzinfo`
    .. |datetime.timedelta().days|                    replace:: :py:attr:`datetime.timedelta.days`
    .. |datetime.timedelta().max|                     replace:: :py:attr:`datetime.timedelta.max`
    .. |datetime.timedelta().microseconds|            replace:: :py:attr:`datetime.timedelta.microseconds`
    .. |datetime.timedelta().min|                     replace:: :py:attr:`datetime.timedelta.min`
    .. |datetime.timedelta().resolution|              replace:: :py:attr:`datetime.timedelta.resolution`
    .. |datetime.timedelta().seconds|                 replace:: :py:attr:`datetime.timedelta.seconds`
    .. |datetime.timezone().max|                      replace:: :py:attr:`datetime.timezone.max`
    .. |datetime.timezone().min|                      replace:: :py:attr:`datetime.timezone.min`
    .. |datetime.timezone().utc|                      replace:: :py:attr:`datetime.timezone.utc`
    .. |datetime.date|                                replace:: :py:class:`datetime.date`
    .. |datetime.date()|                              replace:: :py:class:`datetime.date`
    .. |datetime.datetime|                            replace:: :py:class:`datetime.datetime`
    .. |datetime.datetime()|                          replace:: :py:class:`datetime.datetime`
    .. |datetime.time|                                replace:: :py:class:`datetime.time`
    .. |datetime.time()|                              replace:: :py:class:`datetime.time`
    .. |datetime.timedelta|                           replace:: :py:class:`datetime.timedelta`
    .. |datetime.timedelta()|                         replace:: :py:class:`datetime.timedelta`
    .. |datetime.timezone|                            replace:: :py:class:`datetime.timezone`
    .. |datetime.timezone()|                          replace:: :py:class:`datetime.timezone`
    .. |datetime.tzinfo|                              replace:: :py:class:`datetime.tzinfo`
    .. |datetime.tzinfo()|                            replace:: :py:class:`datetime.tzinfo`
    .. |datetime.MAXYEAR|                             replace:: :py:const:`datetime.MAXYEAR`
    .. |datetime.MINYEAR|                             replace:: :py:const:`datetime.MINYEAR`
    .. |datetime.date().ctime()|                      replace:: :py:func:`datetime.date.ctime`
    .. |datetime.date().fromisocalendar()|            replace:: :py:func:`datetime.date.fromisocalendar`
    .. |datetime.date().fromisoformat()|              replace:: :py:func:`datetime.date.fromisoformat`
    .. |datetime.date().fromordinal()|                replace:: :py:func:`datetime.date.fromordinal`
    .. |datetime.date().fromtimestamp()|              replace:: :py:func:`datetime.date.fromtimestamp`
    .. |datetime.date().isocalendar()|                replace:: :py:func:`datetime.date.isocalendar`
    .. |datetime.date().isoformat()|                  replace:: :py:func:`datetime.date.isoformat`
    .. |datetime.date().isoweekday()|                 replace:: :py:func:`datetime.date.isoweekday`
    .. |datetime.date().replace()|                    replace:: :py:func:`datetime.date.replace`
    .. |datetime.date().strftime()|                   replace:: :py:func:`datetime.date.strftime`
    .. |datetime.date().timetuple()|                  replace:: :py:func:`datetime.date.timetuple`
    .. |datetime.date().today()|                      replace:: :py:func:`datetime.date.today`
    .. |datetime.date().toordinal()|                  replace:: :py:func:`datetime.date.toordinal`
    .. |datetime.date().weekday()|                    replace:: :py:func:`datetime.date.weekday`
    .. |datetime.datetime().astimezone()|             replace:: :py:func:`datetime.datetime.astimezone`
    .. |datetime.datetime().combine()|                replace:: :py:func:`datetime.datetime.combine`
    .. |datetime.datetime().ctime()|                  replace:: :py:func:`datetime.datetime.ctime`
    .. |datetime.datetime().date()|                   replace:: :py:func:`datetime.datetime.date`
    .. |datetime.datetime().dst()|                    replace:: :py:func:`datetime.datetime.dst`
    .. |datetime.datetime().fromisocalendar()|        replace:: :py:func:`datetime.datetime.fromisocalendar`
    .. |datetime.datetime().fromisoformat()|          replace:: :py:func:`datetime.datetime.fromisoformat`
    .. |datetime.datetime().fromordinal()|            replace:: :py:func:`datetime.datetime.fromordinal`
    .. |datetime.datetime().fromtimestamp()|          replace:: :py:func:`datetime.datetime.fromtimestamp`
    .. |datetime.datetime().isocalendar()|            replace:: :py:func:`datetime.datetime.isocalendar`
    .. |datetime.datetime().isoformat()|              replace:: :py:func:`datetime.datetime.isoformat`
    .. |datetime.datetime().isoweekday()|             replace:: :py:func:`datetime.datetime.isoweekday`
    .. |datetime.datetime().now()|                    replace:: :py:func:`datetime.datetime.now`
    .. |datetime.datetime().replace()|                replace:: :py:func:`datetime.datetime.replace`
    .. |datetime.datetime().strftime()|               replace:: :py:func:`datetime.datetime.strftime`
    .. |datetime.datetime().strptime()|               replace:: :py:func:`datetime.datetime.strptime`
    .. |datetime.datetime().time()|                   replace:: :py:func:`datetime.datetime.time`
    .. |datetime.datetime().timestamp()|              replace:: :py:func:`datetime.datetime.timestamp`
    .. |datetime.datetime().timetuple()|              replace:: :py:func:`datetime.datetime.timetuple`
    .. |datetime.datetime().timetz()|                 replace:: :py:func:`datetime.datetime.timetz`
    .. |datetime.datetime().today()|                  replace:: :py:func:`datetime.datetime.today`
    .. |datetime.datetime().toordinal()|              replace:: :py:func:`datetime.datetime.toordinal`
    .. |datetime.datetime().tzname()|                 replace:: :py:func:`datetime.datetime.tzname`
    .. |datetime.datetime().utcfromtimestamp()|       replace:: :py:func:`datetime.datetime.utcfromtimestamp`
    .. |datetime.datetime().utcnow()|                 replace:: :py:func:`datetime.datetime.utcnow`
    .. |datetime.datetime().utcoffset()|              replace:: :py:func:`datetime.datetime.utcoffset`
    .. |datetime.datetime().utctimetuple()|           replace:: :py:func:`datetime.datetime.utctimetuple`
    .. |datetime.datetime().weekday()|                replace:: :py:func:`datetime.datetime.weekday`
    .. |datetime.time().dst()|                        replace:: :py:func:`datetime.time.dst`
    .. |datetime.time().fromisoformat()|              replace:: :py:func:`datetime.time.fromisoformat`
    .. |datetime.time().isoformat()|                  replace:: :py:func:`datetime.time.isoformat`
    .. |datetime.time().replace()|                    replace:: :py:func:`datetime.time.replace`
    .. |datetime.time().strftime()|                   replace:: :py:func:`datetime.time.strftime`
    .. |datetime.time().tzname()|                     replace:: :py:func:`datetime.time.tzname`
    .. |datetime.time().utcoffset()|                  replace:: :py:func:`datetime.time.utcoffset`
    .. |datetime.timedelta().total_seconds()|         replace:: :py:func:`datetime.timedelta.total_seconds`
    .. |datetime.timezone().dst()|                    replace:: :py:func:`datetime.timezone.dst`
    .. |datetime.timezone().fromutc()|                replace:: :py:func:`datetime.timezone.fromutc`
    .. |datetime.timezone().tzname()|                 replace:: :py:func:`datetime.timezone.tzname`
    .. |datetime.timezone().utcoffset()|              replace:: :py:func:`datetime.timezone.utcoffset`
    .. |datetime.tzinfo().dst()|                      replace:: :py:func:`datetime.tzinfo.dst`
    .. |datetime.tzinfo().fromutc()|                  replace:: :py:func:`datetime.tzinfo.fromutc`
    .. |datetime.tzinfo().tzname()|                   replace:: :py:func:`datetime.tzinfo.tzname`
    .. |datetime.tzinfo().utcoffset()|                replace:: :py:func:`datetime.tzinfo.utcoffset`
    .. |datetime|                                     replace:: :py:mod:`datetime`