from __future__ import absolute_import
import sys
import xmlrpc.client
import datetime
import collections
from pprint import pprint
import textwrap
from pytz import timezone
import pytz.reference
import base64
import time

from izaber import config, app_config
from izaber.startup import initializer
import six
from six.moves import range

"""
This module expect the following keys to be present in the zerp.cfg file:

username: USERNAME
password: PASSWORD
database: DATABASE NAME
rpc_url: URL TO /xmlrpc

"""

CUSTOM_CLASSES = {}

class ZerpException(Exception): pass

class InvalidLoginException(ZerpException): pass
class MoreThanOneResult(ZerpException): pass
class ProtocolException(ZerpException): pass

def register_custom_class( model_name, custom_class ):
    """ Create overrides to handle specialized wrappers for
        various classes
    """
    global CUSTOM_CLASSES
    CUSTOM_CLASSES[model_name] = custom_class

class ZerpMetadata(object):
    def __init__(self,model_name,model_data,timezone):
        self._model_name = model_name
        self._model_data = model_data
        self.timezone = timezone

    def dump_schema(self):
        """ Return a string representation of the model schema
        """
        schema = textwrap.dedent("""
        Model: {model} ({name})
        Modules: {modules}
        OSV Memory: {osv_memory}
        Fields:
        {model_fields}
        """).strip()
        md = self._model_data

        field_definition_template = {
            'many2one': "{ttype} -> {relation}",
            'many2many': "{ttype} -> {relation}",
            'one2many': "{ttype} -> {relation}:{relation_field}",
            'float': "{ttype}",
            'reference': "{ttype}",
            'integer': "{ttype}",
            'integer_big': "{ttype}",
            'char': "{ttype}",
            'boolean': "{ttype}",
            'binary': "{ttype}",
            'datetime': "{ttype}",
            'date': "{ttype}",
            'text': "{ttype}",
            'selection': "{ttype}",
        }

        model_fields = []
        for field in md['field_id_records']:
            # Oddly, size doesn't seem to be tracked by the ORM
            field_definition = "  '{field_description}': <{name}{required}> "+field_definition_template[field['ttype']]
            field['required'] = '*' if field['required'] else ''
            model_fields.append(field_definition.format(**field))

        return schema.format(
                        model_fields="\n".join(model_fields),
                        **md
                      )

    def data_normalize(self,value):
      """ Handle weird data formats and convert them into
          something that the Zerp server prefers to use
      """
      if isinstance(value,datetime.datetime):
          # The server uses GMT so we'll need to convert it
          # to that
          timezone = self.timezone
          if not value.tzinfo:
              value = timezone.localize(value)
          datetime_tz = self.timezone.normalize(value)
          datetime_utc = datetime_tz.astimezone(pytz.utc)
          return datetime_utc.strftime('%Y-%m-%d %H:%M:%S')
      elif isinstance(value,Zerp):
          return value.model_name()
      elif isinstance(value,ZerpRecord):
          return value.id
      return value


    def constraint_normalize(self,constraints):
        """ Clean up the constraints so that if there are any
            date objects, they get turned into the string format
            Zerp expects
        """
        filtered_constraints = []
        for constraint in constraints:
            try:
                key, op, value = constraint
                if isinstance(value, collections.Iterable):
                    if not isinstance(value, str):
                        value = [self.data_normalize(v) for v in value]
                else:
                    value = self.data_normalize(value)
                filtered_constraints.append((key, op, value))
            except ValueError:
                # catch elements of constraint list that are boolean
                # operators (e.g. '&', '|')
                if isinstance(constraint, (str, six.text_type)):
                    filtered_constraints.append(constraint)
                else:
                    raise ValueError
        return filtered_constraints

    def dict_data_normalize(self,rec):
        """ Takes a record dict and converts it into something
            that the client update/create like to use
        """
        rec = rec.copy()
        for field_name,field_data in six.iteritems(self.fields()):
            if not field_name in rec: continue
            v = rec[field_name]
            rec[field_name] = self.data_normalize(v)
        return rec

    def fields(self):
        return self._model_data['field_id_lookup']

    def model_name(self):
        return self._model_name

    def __str__(self):
        return self.model_name()

class ZerpClient(object):
    _cache = None

    def __init__(self,
                rpc_url=None,
                username=None,
                password=None,
                database=None,
                cache=None,
                minimal_preload=True,
                debug=False,
                ):
      """ Connect to a new RPC port
      """


      self.username = username
      self._password = password
      self.rpc_url = rpc_url
      self.database = database

      # The setting that controls how much information gets
      # loaded when parameters are requested
      self.minimal_preload = minimal_preload

      # Get the user_id
      try:
          sock_common = xmlrpc.client.ServerProxy(rpc_url+'/common',allow_none=True)
          self.user_id = sock_common.login(
                              self.database,
                              self.username,
                              self._password
                            )
          if not self.user_id:
              raise InvalidLoginException('Invalid Login')
          self.sock = xmlrpc.client.ServerProxy(rpc_url+'/object',allow_none=True)
          self.wizard_sock = xmlrpc.client.ServerProxy(rpc_url+'/wizard',allow_none=True)
          self.report_sock = xmlrpc.client.ServerProxy(rpc_url+'/report',allow_none=True)
          self.db_sock = xmlrpc.client.ServerProxy(rpc_url+'/db',allow_none=True)
      except IOError:
            _, ex, traceback = sys.exc_info()
            message = "Connecting to '%s': %s." % (rpc_url,
                                                   ex.strerror)
            raise IOError(ex.errno, message)


    #### object.* calls

    def execute(self, model, method, *args):
        """ Lets you execute any method on an object.

        For example, this will check availability on packing list id 1234:
        client.execute('stock.picking', 'action_assign', [1234])
        """
        result = self.sock.execute(
                          self.database,
                          self.user_id,
                          self._password,
                          model,
                          method,
                          *args)

        return result

    def exec_workflow(self, model, signal, res_id):
        """ Lets you trigger the workflow on a record.

        For example, this will cancel purchase order 1234:
        client.exec_workflow('purchase.order', 'purchase_cancel', 1234)
        """
        # TODO
        return self.sock.exec_workflow(
            self.database,
            self.user_id,
            self._password,
            model,
            signal,
            res_id)


    #### wizard.* calls
    def wizard_create(self, method, *args):
        """ Instantiates the first step of a wizard
        """
        return self.wizard_sock.create(
            method,
            *args)

    #### report.* calls
    def report(self, object, ids, datas=None, context=None):
        return self.report_sock.report(
            self.database,
            self.user_id,
            self._password,
            object, ids, datas, context)

    def report_get(self, report_id):
        return self.report_sock.report_get(
            self.database,
            self.user_id,
            self._password,
            report_id)

    #### db.* calls
    def migrate_databases(self,databases):
        # FIXME: Probably won't work
        return self.db_sock.migrate_databases(databases)

    #### common.* calls

    def search(self,
               model,
               constraints=[],
               span_start=0,
               span_limit=100000,
               order_by='',
               context=None):
      """ Get a list of ids for records that match the constraints.

      product_ids = client.search(
          'product.product',
          ['|', ('name', 'ilike', 'base assy'),
           ('name', 'ilike', 'LSM Motor Assy')])
      """

      if context is None:
          context = {}
      context.setdefault('lang', u'en_CA')
      context.setdefault('tz', False)

      search_ids = self.execute(
          model,
          'search',
          constraints,
          span_start,
          span_limit,
          order_by,
          context)
      return search_ids

    def fetch(self, model, ids, fields=[]):
        """ Fetch fields for a specific set of records.

        client.fetch('stock.location', [1, 2, 3, 4], ['name'])
        """

        records = self.execute(
            model,
            'read',
            ids,
            fields)
        return records or []

    def search_fetch(
        self,
        model,
        constraints=[],
        fields=[],
        span_start=0,
        span_limit=100000,
        order_by='',
        context=None):
        """ Combine search and fetch in one step.

        product_names = client.search(
            'product.product',
            ['|', ('name', 'ilike', 'base assy'),
             ('name', 'ilike', 'LSM Motor Assy')],
            ['name'])
        """

        search_ids = self.search(
            model,
            constraints,
            span_start,
            span_limit,
            order_by,
            context)
        if len(search_ids) == 0:
            return []
        return self.fetch(model, search_ids, fields)


    def search_fetch_one(
        self,
        model,
        constraints=[],
        fields=[],
        span_start=0,
        span_limit=100000,
        order_by='',
        context=None):
        """ Combine search and fetch in one step.

        This will throw an error if there is more than one result

        product_names = client.search_fetch_one(
            'product.product',
            ['|', ('name', 'ilike', 'base assy'),
             ('name', 'ilike', 'LSM Motor Assy')],
            ['name'])
        """

        search_ids = self.search(
            model,
            constraints,
            span_start,
            span_limit,
            order_by,
            context)
        if len(search_ids) == 0:
            return

        if len(search_ids) != 1:
            raise MoreThanOneResult()

        result = self.fetch(model, search_ids, fields)

        if result: return result[0]
        return

    def update(self, model, ids, to_set):
        """ Update records.

        client.update(
            'stock.location',
            [11],
            {'name': 'doomed location'})
        """

        res = self.execute(
            model,
            'write',
            ids,
            to_set)
        return res

    def create(self, model, fields, context=None):
        """ Create a new record.

        Returns the new record's id.

        client.create(
            'stock.location.path',
            {
                'product_id': 1234,
                'location_from_id': 11,
                'location_dest_id': 23,
                'auto': 'transparent'
            })
        """
        if context == None:
            context = {}
        context.setdefault('lang', u'en_CA')
        context.setdefault('tz', False)
        rec_id = self.execute(
            model,
            'create',
            fields,
            context)
        return rec_id

    def unlink(self, model, ids):
        """ Delete a set of records.

        client.unlink('stock.move', [1, 2, 3, 4])
        """

        return self.execute(
            model,
            'unlink',
            ids)

    def reports_fetch(self, model, ids, context=None ):
        """ Request a report be generated then fetch it!
            The return value should be the decoded data file
        """
        if context is None: context = {}

        generated_report_id = self.report(model,ids,context)

        # The report must be created.
        # Make sure we can generate the report
        reports = []
        for i in range(20):
            time.sleep(0.1)
            report = self.report_get(generated_report_id)
            if report['state']:
                # Normalize the result (take the result string out of
                # base64 encoding)
                report['result'] = base64.decodestring(report['result'])

                # Add it to the list of reports found.
                reports.append(report)
                break

        # Couldn't get it!
        else:
            raise Exception("Couldn't get report!")


        return reports

    def report_fetch_single(self, model, report_id, context=None ):
        reports = self.reports_fetch(model,[report_id],context)
        return reports[0]

class ZerpRecord(object):
    """ Base handler for Zerp records. While it's perfectly possible
        to access records using dicts, this adds a bit of syntax sugar
        on top to make things look a wee bit nicer.
    """
    _rec = {}
    _dirty = {}
    _zerp = None
    _fields = None
    _is_relation = False
    _relation_name = None
    minimal_preload = None

    def __init__(self,
                  zerp,
                  model_metadata,
                  rec,
                  new_record=True,
                  is_relation=False,
                  relation_name=None,
                  minimal_preload=True,
                ):
        self._zerp = zerp
        self._model_metadata = model_metadata
        self._fields = model_metadata.fields()
        self._new_record = new_record
        self._is_relation = is_relation
        self._relation_name = relation_name
        if minimal_preload == None:
            minimal_preload = zerp.minimal_preload
        self.minimal_preload = minimal_preload
        self.load_record(rec)

    def zerp(self):
        """ Return the current ZerpClient object. Wrapped with a reader
            since the code to be able to do obj.zerp is annoying ;)
        """
        return self._zerp

    def dict(self):
        """ Return the dict representation of the data
        """
        import copy
        return copy.deepcopy(self._rec)

    def load_record(self, rec, wipe_dirty=True):
        if isinstance(rec,ZerpRecord):
            self._rec = rec._rec
        else:
            self._rec = rec
        if wipe_dirty:
            self._dirty = {}

    def record_data(self):
        return self._rec

    def is_dirty(self):
        return len(self._dirty)>0

    def fields(self):
        return self._fields

    def _commit_new(self):
        """ If a record is marked a being new. Let's add it to the
            database
        """

        if not self._new_record: return

        # Attempt to add the new record to the database
        new_rec = self._rec.copy()
        new_rec.update(self._dirty)

        rec_id = self._zerp.create(new_rec)
        if not rec_id: return

        # Load the new record with all the defaulted values
        new_rec = self._zerp.fetch_single(rec_id)
        if not new_rec: return
        self.load_record(new_rec)

        # Finally we can say we're done with this task
        self._new_record = False
        return self

    def _commit_update(self):
        """ If a record has to be updated, let's update the database
        """
        if 'id' not in self._rec: return
        result = self._zerp.update(
          [self.id],
          self._dirty
        )
        self._dirty = False
        return result

    def commit(self):
        if self._new_record:
            return self._commit_new()
        if self.is_dirty():
            return self._commit_update()

    def __getitem__(self,attr):
        # A way to support many2one relationships
        # so that when record[0] or record[1] are called
        # it reflects what you can get from record.dict()
        if self._is_relation:
            if attr == 0:
                return self.id
            elif attr == 1:
                return self._relation_name
        return self.__getattr__(attr)

    def __getattr__(self,attr):
        if attr in self._fields:
            field = self._fields[attr]
            # Attribute is in fields but not in _rec?
            # This means that the data hasn't been fully loaded
            # so we'll lazy load the rest of the info now.
            # If we have minimal_preload turned on, we don't load
            # much at all
            if not attr in self._rec:
                if self.minimal_preload:
                    rec = self._zerp.fetch_single(self._rec['id'],[attr])
                    self._rec[attr] = rec[attr]
                else:
                    rec = self._zerp.fetch_single(self._rec['id'])
                    self.load_record(rec)

            if not attr in self._rec:
              AttributeError("Could not load data for field: %s" % attr)

            value = self._rec[attr]
            if field['ttype'] == 'many2one':
              if not value: return
              return self._zerp.get_model(field['relation']).record_instantiate(
                {
                    'id': value[0],
                },
                is_relation=True,
                relation_name=value[1],
                minimal_preload=self.minimal_preload,
              )
            elif field['ttype'] == 'many2many':
              if not value: return []
              return self._zerp.get_model(field['relation']).fetch(value)
            elif field['ttype'] == 'one2many':
              if not value: return []
              return self._zerp.get_model(field['relation']).fetch(value)
            elif field['ttype'] == 'reference':
              pass
            elif field['ttype'] == 'datetime':
              # The incoming data is actually in GMT so we'll go through that
              # then convert to the timezone the client actually uses
              value = pytz.timezone('utc').localize(
                              datetime.datetime.strptime(value,'%Y-%m-%d %H:%M:%S')
                          )\
                          .astimezone(self._zerp.timezone)
            elif field['ttype'] == 'date':
              if isinstance(value,datetime.datetime) or isinstance(value,datetime.date):
                    pass
              else:
                  value = self._zerp.timezone.localize(
                                  datetime.datetime.strptime(value,'%Y-%m-%d')
                              )

            return value

        if attr in self._rec:
          return self._rec[attr]

        raise AttributeError("%s has no field %s" % (self._zerp.model_name(), attr))


    def __setitem__(self,attr,value):
        return self.__setattr__(attr,value)

    def __setattr__(self,attr,value):
        if attr[0] != '_' and \
          ( attr in self._fields
              or
              attr in ('name') # Handle the special case of a "name"
          ):
            self._dirty[attr] = value
            self._rec[attr] = value
            return value
        return super(ZerpRecord,self).__setattr__(attr,value)

    def __repr__(self):
        if 'id' in self._rec:
            if 'name' in self._rec:
                return u"%s<%i:%s>"%(self._zerp,self.id,self._rec['name'])
            else:
                return u"%s<%i>"%(self._zerp,self.id)
        else:
            return u"%s" % self._zerp

class Zerp(object):
    _model_metadata = None
    client = None
    minimal_preload = None

    def __init__(
            self,
            client=None,
            model_metadata=None,
            cache=None,
            debug=False,
            timezone=timezone('America/Vancouver'),
            minimal_preload=True,
            **client_kwargs
          ):

        self.client = client
        self.client_kwargs = client_kwargs

        self.timezone = timezone
        self.minimal_preload = minimal_preload

        self._model_metadata = model_metadata
        self._debug = debug

        self.reset(cache=cache)

    def connect(self,**kwargs):
        """ Start the conversation with the remote ZERP server.
        """
        if self.client:
            return self.client

        if not kwargs:
            kwargs = self.client_kwargs

        self.client = ZerpClient(**kwargs)

    def reset(self,cache=None):
        """ Clear out the cache, do all that's required for
            a fresh object
        """
        self._cache = cache or {}

    def get_model(self,model_name,
                    zerp_class=None,
                    minimal_preload=None,
                    *args,**kwargs):
        """
          :param model_name: Zerp model name
          :param zerp_class: Override class for handling the model
          :param minimal_preload: Boolean, should many2one fields be fully loaded when accessed?
        """
        model_metadata = self.model_metadata_load(model_name)
        if zerp_class == None: zerp_class = CUSTOM_CLASSES.get(model_name,Zerp)
        if minimal_preload == None: minimal_preload = self.minimal_preload
        return zerp_class(
                    client=self.client,
                    model_metadata=model_metadata,
                    cache=self._cache,
                    timezone=self.timezone,
                    minimal_preload=minimal_preload,
                  )
    get = get_model

    def fields(self):
        return self._model_metadata.fields()

    def dict_data_normalize(self,data):
        return self._model_metadata.dict_data_normalize(data)

    def report_fetch_single(self,*argv,**kwargs):
        if self._model_metadata == None: raise Exception('No Model Defined!')
        return self.client.report_fetch_single(self._model_metadata.model_name(),*argv,**kwargs)


    def unlink(self,*argv,**kwargs):
        if self._model_metadata == None: raise Exception('No Model Defined!')
        return self.client.unlink(self._model_metadata.model_name(),*argv,**kwargs)

    def create(self,fields,context=None,*argv,**kwargs):
        if self._model_metadata == None: raise Exception('No Model Defined!')
        fields = self.dict_data_normalize(fields)

        if context == None: context = {}
        context.setdefault('tz',self.timezone.zone)
        return self.client.create(self._model_metadata.model_name(),fields,context,*argv,**kwargs)

    def insertion_record(self,record={}):
        return self.record_instantiate(record,new_record=True)

    def update(self,ids,to_set,*argv,**kwargs):
        if self._model_metadata == None: raise Exception('No Model Defined!')
        to_set = self.dict_data_normalize(to_set)
        return self.client.update(self._model_metadata.model_name(),ids,to_set,*argv,**kwargs)

    def fetch(self,*argv,**kwargs):
        if self._model_metadata == None: raise Exception('No Model Defined!')
        records = self.client.fetch(self._model_metadata.model_name(),*argv,**kwargs)
        return self.records_list_create(records)

    def fetch_single(self,rec_id,*args,**kwargs):
        """ Looks for a single record identified by its ID number
        """
        if self._model_metadata == None: raise Exception('No Model Defined!')
        records = self.client.fetch(self._model_metadata.model_name(),[rec_id],*args,**kwargs)
        if len(records) != 1: return
        return self.record_instantiate(records[0])

    def search(self,constraints=[],*argv,**kwargs):
        if self._model_metadata == None: raise Exception('No Model Defined!')
        constraints = self._model_metadata.constraint_normalize(constraints)
        return self.client.search(self._model_metadata.model_name(),constraints,*argv,**kwargs)

    def search_fetch(
            self,
            constraints=[],
            *args,
            **kwargs
        ):
        if self._model_metadata == None: raise Exception('No Model Defined!')
        constraints = self._model_metadata.constraint_normalize(constraints)
        records = self.client.search_fetch(self._model_metadata.model_name(),constraints,*args,**kwargs)
        return self.records_list_create(records)

    def search_fetch_one(
            self,
            constraints=[],
            *args,
            **kwargs
        ):
        if self._model_metadata == None: raise Exception('No Model Defined!')
        constraints = self._model_metadata.constraint_normalize(constraints)
        record = self.client.search_fetch_one(self._model_metadata.model_name(),constraints,*args,**kwargs)
        if not record: return
        return self.record_instantiate(record)


    def records_list_create(self,rec_list):
        """ Takes a list of records from a resultset and
            turns it into a list of ZerpRecord objects
        """
        return [ self.record_instantiate(rec) for rec in rec_list]

    def record_instantiate(self,rec,
                            new_record=False,
                            is_relation=False,
                            relation_name=None,
                            minimal_preload=None,
                            ):
        """ Just makes the creation of a ZerpRecord object easier
        """
        if minimal_preload == None:
            minimal_preload = self.minimal_preload
        return ZerpRecord(
            zerp=self,
            model_metadata=self._model_metadata,
            rec=rec,
            new_record=new_record,
            is_relation=is_relation,
            relation_name=relation_name,
            minimal_preload=minimal_preload,
        )

    def dump_schema(self):
        """ Return a string representation of the model schema
        """
        if not self._model_metadata:
            return self._model_metadata.dump_schema()
        else:
            return None


    def model_name(self):
        """ Name of the model we are referencing
        """
        if self._model_metadata:
            return self._model_metadata.model_name()
        else:
            return None

    def model_metadata_load(self,model_name,force_reload=False):
        """ Load up the model data (use the cached entries
            if available)
        """
        if not model_name in self._cache:
            model_data = self.client.search_fetch(
                                          'ir.model',
                                          [('model','=',model_name)],
                                          [
                                              'name',
                                              'field_id',
                                              'model',
                                              'modules',
                                              'osv_memory',
                                          ]
                                        )[0]
            model_field_ids = model_data['field_id']
            model_data['field_id_records'] = self.client.search_fetch(
                                                'ir.model.fields',
                                                [('id','in',model_field_ids)],
                                                [
                                                    'name',
                                                    'ttype',
                                                    'required',
                                                    'field_description',
                                                    'relation',
                                                    'relation_field',
                                                ]
                                              )


            field_id_lookup = {}
            for field_rec in model_data['field_id_records']:
                field_id_lookup[field_rec['name']] = field_rec
            model_data['field_id_lookup'] = field_id_lookup

            self._cache[model_name] = ZerpMetadata(
                                          model_name,
                                          model_data,
                                          self.timezone
                                        )
        return self._cache[model_name]

    def __str__(self):
        """ Useful information on the object is converted to a str (eg. printed)
        """
        if not self.client:
            return "Zerp<{}>".format(self.model_name() or 'None')
        return "Zerp<%s@%s:%s>" % (
                  self.model_name() or 'None',
                  self.client.rpc_url,
                  self.client.database
                )

    def object_exec(self,method,*args,**kwargs):
        """ Attempt to execute an ORM method
        """
        if self._model_metadata == None: raise Exception('No Model Defined!')
        return self.client.execute(
                  self._model_metadata.model_name(),
                  method,
                  *args,
                  **kwargs
              )

    def __getattr__(self,k):
        """ Proxy an ORM method through to the invoker
        """
        return lambda *a,**kw: self.object_exec(k,*a,**kw)

class ZerpUser(Zerp):
    """ Provide additional helpful support for res.users records
    """

    def user_from_login(self,login):
        """ Returns the numeric user_id value for the login provided
        """
        user_ids = self.search([('login','=',login)])
        if user_ids and len(user_ids) == 1:
            return self.fetch_single(user_ids[0])
        return

register_custom_class('res.users', ZerpUser)


zerp = Zerp()

@initializer('zerp')
def load_config(**options):
    if not config.get('zerp'):
        import textwrap
        raise Exception(textwrap.dedent('''
        config.zerp has not been defined in izaber.yaml. Try defining it with something
        like:

        default:
          zerp:
            username: USERNAME
            password: PASSWORD
            database: DATABASE NAME
            rpc_url: https://zerp6.izaber.com/xmlrpc

        '''))
    client_options = config.zerp.dict()
    zerp.connect(**client_options)

