from __future__ import absolute_import
import datetime, calendar, dateutil.parser

from izaber.zerp import *
from six.moves import map

class AnalyticsException(Exception):
    pass

class Timesheet(object):
    def __init__(self,zerp,ts_rec):
        self.zerp = zerp
        self._ts_rec = ts_rec
        self.id = ts_rec.id
        self.employee_id = ts_rec.employee_id.id
        self.date_from = ts_rec.date_from.replace(hour=0,minute=0,second=0)
        self.date_to = ts_rec.date_to.replace(hour=23,minute=59,second=59)
        self.date_current = ts_rec.date_current
        self.state = ts_rec.state

        # Need to learn some more stuff about the employee
        # to be able to append entries to the analytic accounts
        emp_model = zerp.get_model('hr.employee')
        emp_rec = emp_model.fetch_single(
                        self.employee_id,
                        [
                            'product_id',
                            'journal_id',
                            'uom_id',
                            'user_id',
                            'department_id',
                        ]
                    )
        self.emp_rec = emp_rec

        # For the sake of speed, a very crunchy way of loading
        tmpl_rec = emp_rec.product_id.product_tmpl_id
        a = tmpl_rec.property_account_expense \
              or tmpl_rec.categ_id.property_account_expense_categ
        self.general_account_id = a.id

        # And preload information we'll need
        self.load()

    def is_present(self):
        """ Returns true if the user is marked as "signed in" for the
            current timesheet. This really only useful for timesheets
            that are open. Confirmed or completed timesheets should
            have their last attendance entry as "sign_out"
        """
        attend_entries = list(self._attend_entries)
        attend_entries.reverse()
        for attend in attend_entries:
            if attend.action == 'sign_in':
                return True
            elif attend.action == 'sign_out':
                return False
        return False


    def now(self):
        """ Return the current datetime with the timezone information attached
        """
        return self.zerp.timezone.localize(datetime.datetime.now())

    def now_daily_hours(self):
        """ Convert H:M:S into a single floating point number
            that represents the number of hours since 0000. Used
            for calculations regarding time spans.
        """
        now = self.now()
        hours = (now.hour +
                 now.minute / 60.0 +
                 now.second / 3600.0)
        return hours


    def date_within_frame(self,timestamp=None):
        """ Checks the date to see it's within the
            range of the current timesheet.
            This throws an exception of the timestamp is outside
            of the allowed range

            :param timestamp: datetime/str of requested timestamp
            :returns timestamp: the timestamp if okay

        """
        if timestamp == None:
            timestamp = self.date_current
        elif not isinstance(timestamp,datetime.datetime):
            timestamp = dateutil.parser.parse(timestamp)
        if not timestamp.tzinfo:
            timestamp = self.zerp.timezone.localize(timestamp)

        # Do some boundary checks
        if timestamp > self.date_to:
            raise Exception(
                    "Sorry, timestamp ({:%Y-%m-%d %H:%M:%S}) "\
                    "later than the current timesheet's range ({:%Y-%m-%d %H:%M:%S}).".format(
                      timestamp, self.date_to
                    )
                  )
        elif timestamp < self.date_from:
            raise Exception(
                    "Sorry, timestamp ({:%Y-%m-%d %H:%M:%S}) "\
                    "earlier than the current timesheet's range ({:%Y-%m-%d %H:%M:%S}).".format(
                      timestamp, self.date_from
                    )
                  )

        return timestamp

    def load_attendances(self):
        """ Load the attendance information and cache it
            This returns the information in chronological order (So element 0 is the newest)
        """
        # Load the information related to when the user has clocked in and out
        attend_model = self.zerp.get_model('hr.attendance')
        attend_entries = attend_model.search_fetch(
                            [
                              ('sheet_id','=',self.id),
                            ],
                            ['action','name','day','daily_hours'],
                          )
        self._attend_entries = sorted(attend_entries,key=lambda a:a.name)
        return self._attend_entries

    def load_hr_analytics(self):
        """ Load the account analytic lines that document what activies
            users were performing while signed in
        """
        # Load the data assocated with what the user had been doing during that time
        hat_model = self.zerp.get_model('hr.analytic.timesheet')
        hat_hits = hat_model.search_fetch(
                                [('sheet_id','=',self.id)],
                                ['line_id']
                              )
        hr_hits = []
        if hat_hits:
            aal_model = self.zerp.get_model('account.analytic.line')
            aal_ids = [h.line_id.id for h in hat_hits]
            aal_hits = aal_model.search_fetch(
                          [('id','in',aal_ids)],
                          [
                            'journal_id',
                            'general_account_id',
                            'product_id',
                            'account_id',
                            'user_id',
                            'date',
                            'unit_amount',
                            'name'
                          ]
                        )
            aal_lookup = {}
            for aal in aal_hits:
                aal_lookup[aal.id] = aal
            for hat in hat_hits:
                line = {
                    'account.analytic.line': aal_lookup.get(hat.line_id.id),
                    'hr.analytic.timesheet': hat,
                }
                hr_hits.append(line)
        self._hr_analytics = hr_hits
        return hr_hits

    def load_analytics(self):
        """ Load the account analytic lines that document what activies
            users were performing while signed in
        """
        # Load the data assocated with what the user had been doing during that time
        hat_model = self.zerp.get_model('hr.analytic.timesheet')
        hat_hits = hat_model.search_fetch(
                                [('sheet_id','=',self.id)],
                                ['line_id']
                              )
        if hat_hits:
            aal_model = self.zerp.get_model('account.analytic.line')
            aal_ids = [h.line_id.id for h in hat_hits]
            aal_hits = aal_model.search_fetch(
                          [('id','in',aal_ids)],
                          [
                            'journal_id',
                            'general_account_id',
                            'product_id',
                            'account_id',
                            'user_id',
                            'date',
                            'unit_amount',
                            'name'
                          ]
                        )
        else: aal_hits = []
        self._analytics = aal_hits
        return aal_hits

    def load(self):
        """ This loads the all the information related to the timesheet
            that we may want to access
        """
        self.load_attendances()
        self.load_analytics()

    def sign_in(self,timestamp=None):
        """ Try and mark the employee as signed in on
            the timesheet
        """
        if timestamp == None:
            timestamp = datetime.datetime.now()
        timestamp = self.date_within_frame(timestamp)
        attend_model = self.zerp.get_model('hr.attendance')
        attend_model.create({
            'name': timestamp,
            'action': 'sign_in',
            'sheet_id': self.id,
            'employee_id': self.employee_id,
            'day': timestamp.strftime('%Y-%m-%d'),
        })
        self.load_attendances()

    def sign_out(self,timestamp=None):
        """ Try and mark the employee as signed out on
            the timesheet
        """
        if timestamp == None:
            timestamp = datetime.datetime.now()
        timestamp = self.date_within_frame(timestamp)
        attend_model = self.zerp.get_model('hr.attendance')
        attend_model.create({
            'name': timestamp,
            'action': 'sign_out',
            'sheet_id': self.id,
            'employee_id': self.employee_id,
            'day': timestamp.strftime('%Y-%m-%d'),
        })
        self.load_attendances()

    def attendances_delete(self,attend_ids=None):
        """ Try and remove attendances based upon id
        """
        if not attend_ids: return
        attend_model = self.zerp.get_model('hr.attendance')
        attend_model.unlink(attend_ids)
        self.load_attendances()

    def attendances(self,date=None):
        """ Finds the current recorded events for the
            day

            :param date: timestamp of the date in question
            :returns list: list of attendance records sorted
                           in chronological order

            The way attendance records connect:

              hr_timesheet_sheet.sheet,id
                -> hr.attendance,sheet_id
        """
        if date == None:
            return self._attend_entries

        date = self.date_within_frame(date)
        date_str = date.strftime('%Y-%m-%d')

        attend_entries = []
        for entry in self._attend_entries:
            if entry.day == date_str:
                attend_entries.append(entry)
        return sorted(attend_entries,key=lambda a:a.name)

    def analytics_delete(self,aal_ids=None):
        """ Delete analytics entry
        """
        if not aal_ids: return
        aal_model = self.zerp.get_model('account.analytic.line')
        aal_model.unlink(aal_ids)
        hat_model = self.zerp.get_model('hr.analytic.timesheet')
        hat_ids = hat_model.search([('line_id','in',aal_ids)])
        if hat_ids:
            hat_model.unlink(hat_ids)
            self.load_analytics()

    def analytics(self,date=None,date_from=None,date_to=None):
        """
            hr_timesheet_sheet.sheet,id -> hr.analytic.timesheet,sheet_id
               hr.analytic.timesheet,line_id -> account.analytic.line,id

            While it won't happen, there's a many to many relationship
            that's possible. In practice, and in code, the entries are
            one to many
        """

        if not self._analytics:
            return []

        analytics = list(self._analytics)

        # Figure out which Analytic entries are correct for the day
        if date:
            date = self.date_within_frame(date)
            date_str = date.strftime('%Y-%m-%d')
            filtered_analytics = []
            for analytic in analytics:
                if analytic.date.strftime('%Y-%m-%d') == date_str:
                    filtered_analytics.append(analytic)
            return filtered_analytics
        else:
            if date_from:
                date_from = self.date_within_frame(date_from)
                date_from_str = date_from.strftime('%Y-%m-%d')
                filtered_analytics = []
                for analytic in analytics:
                    if analytic.date >= date_from_str:
                        filtered_analytics.append(analytic)
                analytics = filtered_analytics

            if date_to:
                date_to = self.date_within_frame(date_to)
                date_to_str = date_to.strftime('%Y-%m-%d')
                filtered_analytics = []
                for analytic in analytics:
                    if analytic.date <= date_to_str:
                        filtered_analytics.append(analytic)
                analytics = filtered_analytics

        return analytics

    def analytic_account_id_by_name(self,name):
        """ This attempts to find a single analytic acount
            based upon the name.
        """
        aaa_model = self.zerp.get_model('account.analytic.account')
        aaa_ids = aaa_model.search([('name','ilike',"{}".format(name))])
        if len(aaa_ids) == 1:
            return aaa_ids[0]
        if len(aaa_ids) == 0:
            raise AnalyticsException('No matching analytic account found for {}'.format(name))

        raise AnalyticsException('More than one analytic account found!')

    def log(self,timestamp,analytic_id,description,unit_amount):
        """ Log an event to the current timesheet day
        """
        if timestamp == None:
            timestamp = datetime.datetime.now()
        timestamp = self.date_within_frame(timestamp)
        day = timestamp.strftime('%Y-%m-%d')

        if not isinstance(analytic_id,int):
            analytic_id = self.analytic_account_id_by_name(analytic_id)

        # Then create the analytic entry
        aal_model = self.zerp.get_model('account.analytic.line')
        emp_rec = self.emp_rec
        aal_id = aal_model.create({
             'journal_id': emp_rec.journal_id.id,  # timesheet journal
             'general_account_id': self.general_account_id, # usually wages
                                                            # account
             'product_id': emp_rec.product_id.id, # labour product
             'product_uom_id': emp_rec.uom_id.id, # the unit of measure for
                                                  # the product. ('Hours')
             'user_id': emp_rec.user_id[0], # The user associated with this
                                         # record. Should be the same as
                                         # timesheet
             'date': day, # When this happened
             'account_id': analytic_id, # Analytic Account ID
             'unit_amount': unit_amount, # hours worked
             'name': description, # description
        })

        # And link the analytic entry with the user's
        # timesheet
        hat_model = self.zerp.get_model('hr.analytic.timesheet')
        hat_id = hat_model.create({
            'line_id': aal_id,
            'sheet_id': self.id,
            'account_id': analytic_id,
            'journal_id': emp_rec.journal_id.id
        })

        return hat_id

    def log_activity(self,timestamp,analytic_id,description):
        """ Log an event to the current timesheet day
        """
        if timestamp == None:
            timestamp = self.now()
        timestamp = self.date_within_frame(timestamp)
        day = timestamp.strftime('%Y-%m-%d')

        # We'll do things the way that Zerp does it.
        # Basically, it finds the last event in the day
        # then finds the delta to the timestamp requested.
        # It uses that delta to insert an analytic entry
        # into the database

        # We load the attendances so that we have a fresh copy to
        # perform a delta with.
        self.load_attendances()

        # So first, we need to find the day's current events
        attendance = self.attendances(day)
        if not attendance or attendance[-1].action == 'sign_out':
            raise Exception('You must be signed in!')
        last_event_time = attendance[-1].name

        # Can finally figure out how much time has passed since
        # the previous event
        time_delta = timestamp - last_event_time
        hours_delta = time_delta.total_seconds()/(60.0*60.0)

        if hours_delta <= 0:
            raise Exception('Time for logging conflicts '
                    +'with existing attendance records!')

        # This logs to the analytic tables
        self.log(timestamp,analytic_id,description,hours_delta)
        self.load_analytics()

        # And this logs the action in the attendances
        attend_model = self.zerp.get_model('hr.attendance')
        attend_model.create({
            'name': timestamp,
            'action': 'action',
            'sheet_id': self.id,
            'employee_id': self.employee_id,
            'day': day
        })

        # We load it again just so that what gets displayed to the
        # user is consistant with what's in Zerp
        self.load_attendances()

    def elapsed_hours(self):
        """ Return the amount of time that has passed since the
            last action
        """
        attendances = self.attendances()
        if not attendances: return 0
        last_attendance = attendances[-1]
        today = self.now().strftime('%Y-%m-%d')
        if today != last_attendance.day:
            return 0
        daily_hours = self.now_daily_hours()
        return daily_hours - abs(last_attendance.daily_hours)


    def totals(self,date=None):
        """ Returns the total attendances/logged hour information
            on a day by day basis
        """

        # Get a list of all the attendance entries
        self.load_attendances()
        attend_entries = self._attend_entries

        attendances = {}
        attendances_by_day = {}
        for entry in attend_entries:
            if entry.action not in ['sign_in','sign_out']:
                continue
            attendances.setdefault(entry.day,0)
            attendances[entry.day] += entry.daily_hours
            attendances_by_day.setdefault(entry.day,[])\
                              .append(entry)

        # Get a list of analytic entries for the period
        analytic_entries = self.analytics()
        analytics = {}
        for entry in analytic_entries:
            date_str = entry.date.strftime('%Y-%m-%d')
            analytics.setdefault(date_str,0)
            analytics[date_str] += entry.unit_amount

        # Now show the info?
        totals_by_day = {}
        dates = set(list(attendances.keys())+list(analytics.keys()))
        if date:
            date_str = date.strftime('%Y-%m-%d')
        for day in sorted(dates):
            ttl_attend = attendances.get(day,0)
            ttl_analytic = analytics.get(day,0)
            if date and date_str != day:
                continue
            totals_by_day[day] = {
                'total_attendance': ttl_attend,
                'total_difference': ttl_attend-ttl_analytic,
                'total_timesheet': ttl_analytic
            }

        # Adjust the totals if required. Basically
        # the day is today and the user hasn't signed out
        # we'll just treat it as if the sign out was performed
        # at just this moment.
        today = self.now().strftime('%Y-%m-%d')
        if today in totals_by_day:
            if today in attendances_by_day \
              and attendances_by_day[today][-1].action != 'sign_out':
                daily_hours = self.now_daily_hours()
                totals_by_day[day]['total_attendance'] += daily_hours
                totals_by_day[day]['total_difference'] += daily_hours

        return totals_by_day

class TimesheetModel(Zerp):

    def timesheet_from_id(self,id):
        """ Based upon the id, load timesheet data and instantiate the
            management object
        """
        ts_rec = self.fetch_single(
            id,
            [
                'id',
                'state',
                'date_to',
                'date_from',
                'date_current',
                'employee_id',
            ]
        )
        ts = Timesheet(self,ts_rec)
        return ts

    def timesheet(self,id=None,employee_id=None,date=None):
        """ Returns the timesheet object that allows the
            manipulation of the particular timesheet

            :param id: Direct access, use the ID of the record
            :param employee_id: the hr.employee id for the record. If not
                            specified, the current logged in user's
                            hr.employee id will be used
            :param date: Get the timesheet that's appropriate for
                          this particular day. If not specified,
                          the 'current_date' on the timesheet will be used.
        """

        if employee_id == None:
            hre_model = self.get_model('hr.employee')
            hre_rec = hre_model.search_fetch_one(
                          [
                            ('user_id','=',self.client.user_id)
                          ],
                          ['id','department_id']
                        )
            employee_id = hre_rec.id

        if date == None:
            date = datetime.datetime.now()
        elif not isinstance(date,datetime.datetime):
            date = dateutil.parser.parse(date)

        ts_ids = self.search([
                      ('date_from','<=',date.strftime('%Y-%m-%d')),
                      ('date_to','>=',date.strftime('%Y-%m-%d')),
                      ('employee_id','=',employee_id),
                  ])


        if ts_ids:
            return self.timesheet_from_id(ts_ids[0])

        # So, we didn't find the timesheet so let's
        # try and create one for the user.

        # IMPORTANT:
        # We will not be relying on the default date span settings
        # provided by Zerp. They use the current date and have
        # no provision for automagic dates. The way Zaber handles
        # timesheets is every fortnight in the addon
        # zaber-custom/hr_timesheet_semimonthly and this code
        # attempts to replicate the behaviour.

        # Need to know the user's department ID
        hre_model = self.get_model('hr.employee')
        hre_rec = hre_model.search_fetch_one(
                      [
                        ('user_id','=',self.client.user_id)
                      ],
                      ['department_id']
                    )
        department_id = hre_rec.department_id.id

        year = date.year
        month = date.month
        day = date.day
        d = lambda d: datetime.datetime(year,month,d)
        if day <= 15:
            date_from = d(1)
            date_to = d(15)
        else:
            (day_start,day_end) = calendar.monthrange(date.year,date.month)
            date_from = d(16)
            date_to = d(day_end)

        # Need to know more information from the employee for this to work...
        ts_id = self.create({
                      'employee_id': employee_id,
                      'department_id': department_id,
                      'state': 'new',
                      'date_from': date_from,
                      'date_to': date_to,
                      'date_current': date,
                      'company_id': 1, # FIXME - hard code
                  })

        return self.timesheet_from_id(ts_id)

    def timesheet_submit(self,*ts_ids):
        """ If the timesheet is in draft mode, this is equivalent to
            clicking on the "Submit" button. This lets HR and
            accounting know that this timesheet is ready for processing.

            DEBUG_RPC:rpc.request:
              (
                'execute', 
                DATABASE, 
                UID, 
                PASSWORD, 
                (
                  'hr_timesheet_sheet.sheet', 
                  'button_confirm', 
                  [ID], 
                  context
                ))
        """

        # FIXME: Return None or raise exception?
        if not ts_ids: return
        return self.object_exec(
                    'button_confirm',
                    list(map(int,ts_ids)),
                )

    def timesheet_reject(self,ts_id,force=False):
        """ If the timesheet is in submit mode, this is equivalent to
            clicking on the "Reject" button. This lets HR and
            accounting return control of a timesheet back to the user

            If force is False, the timesheet will only be rejected
            when the timesheet is in the state of "confirm"

            DEBUG_RPC:rpc.request:
              (
                'exec_workflow',
                DATABASE,
                UID,
                PASSWORD,
                (
                  'hr_timesheet_sheet.sheet',
                  'cancel',
                  ID
                )
              )
        """

        # FIXME: Return None or raise exception?
        if not ts_id: return

        if not force:
            ts_rec = self.fetch_single(ts_id,['state'])
            if not ts_rec: return
            if ts_rec['state'] != 'confirm': return

        return self.object_exec_workflow(
                    'cancel',
                    int(ts_id)
                )


register_custom_class('hr_timesheet_sheet.sheet', TimesheetModel)

