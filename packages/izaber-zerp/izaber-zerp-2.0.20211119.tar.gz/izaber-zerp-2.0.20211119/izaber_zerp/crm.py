from __future__ import absolute_import
from __future__ import print_function
from zaber.zerp import *
import operator
import sys
import six
from six.moves import range


try:
    # Note that this requires python-Levenshtein to  be installed
    # apt-get install python-levenshtein
    import Levenshtein
except ImportError:
    pass


def levenshtein(s1, s2):
    """ Calculate how different two strings are.

    Returns a number representing the differences. The lower the number, the
    more similar they are.
    Source: http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
    """

    if 'Levenshtein' in sys.modules:
        return Levenshtein.distance(s1,s2)

    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if not s1:
        return len(s2)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

SUFFIXES = [
    u' inc',
    u', inc',
    u' inc.',
    u', inc.',
    u' ltd',
    u', ltd',
    u' ltd.',
    u', ltd.',
    u' llc',
    u', llc']

def zerp_simplify_name(name):
  simple = six.text_type(name).strip().lower()
  for suffix in SUFFIXES:
    if simple.endswith(suffix):
      simple = simple[:-len(suffix)]
      break
  return simple

class ZerpPartner(Zerp):
  """ Provide additional helpful support for res.partner records
  """

  _simple_partner_names_list = False

  def simple_partner_names_list(self, preload=None):
      if not self._simple_partner_names_list:
          # Create a lookup list of partners in the system
          partners = []
          for partner in self.search_fetch([('active','in',['t','f'])],['id','name','active']):
              partners.append({
                  'partner_id': partner.id,
                  'partner_name': partner.name,
                  'active': partner.active,
                  'simple_name': zerp_simplify_name(partner.name),
              })
          self._simple_partner_names_list = partners
      return self._simple_partner_names_list

  def find_similar_company_names(self, company_name):
      """ Given a company name, compare against the Zerp database and see if
          we can't find a company that's similarly named
      """
      partners = self.simple_partner_names_list()

      new_names = []

      new_name = company_name.strip()
      simple_new_name = zerp_simplify_name(new_name)
      cutoff = len(simple_new_name)
      best_names = [({}, cutoff), ({}, cutoff), ({}, cutoff)]
      for partner in partners:
          diff = levenshtein(simple_new_name, partner['simple_name'])
          index = 3
          while (index > 0 and diff < best_names[index-1][1]):
              index -= 1
          if index < 3:
              partner_data = partner.copy()
              partner_data['score'] = diff
              best_names.insert(index, (partner_data, diff))
              del best_names[3]

      results = []
      for result in best_names:
          results.append(result[0])

      return results

      results = {
          'simple_name': simple_new_name,
          'best_partners': best_names,
          'diff': best_names[0][1],
          'partner_id': best_names[0][0]['partner_id'],
      }

      return results



  def find_matches(self, contacts):
    """ Given a list of names, attempt to find all the matches for partners and
        contacts

        contacts should be an array of dicts. Each dict should have at minimum the
        following keys:

        contacts = [
          {
            'Company': name of company
            'First Name': User's firstname
            'Last Name': User's lastname
          }
          ...
        ]
    """

    # Create a lookup list of partners in the system
    partners = self.simple_partner_names_list()

    # Now, iterate through the contacts to see what
    # matches we may find...
    new_names = []
    for contact in contacts:
        new_name = contact['Company'].strip()
        contact_name = contact['First Name'] + u' ' + contact['Last Name']
        if not new_name:
            new_name = contact_name
        simple_new_name = zerp_simplify_name(new_name)
        cutoff = len(simple_new_name)
        best_names = [({}, cutoff), ({}, cutoff), ({}, cutoff)]
        for partner in partners:
            diff = levenshtein(simple_new_name, partner['simple_name'])
            index = 3
            while (index > 0 and diff < best_names[index-1][1]):
                index -= 1
            if index < 3:
                best_names.insert(index, (partner, diff))
                del best_names[3]
        entry = {
            'name': new_name,
            'contact': contact_name,
            'best_partners': best_names,
            'diff': best_names[0][1]
        }
        new_names.append(entry)
    new_names.sort(key=operator.itemgetter('diff'))
    return new_names

register_custom_class('res.partner', ZerpPartner)

IGNORED_STATES = (
    u'13|VIENNA', #Austria
    u'29|SP',   #Brazil
    u'29|SAO PAULO', #Brazil
    u'29|PE',   #Brazil
    u'41|NEUCHATEL', #Switzerland
    u'46|PR CHINA', #China
    u'56|NRW', #Germany
    u'74|0',    #France
    u'101|TAM', #India
    u'101|GUJ',
    u'101|KAR',
    u'109|FUKUOKA PREFECTURE', #Japan
    u'109|IBARAKI', #Japan
    u'117|SEOUL', #Korea
    u'117|SEO', #Korea
    u'117|DAE', #Korea
    u'117|KYO', #Korea
    u'117|PUS', #Korea
    u'128|VIL', #Lithuania
    u'150|PUE', #Mexico
    u'150|YU',  #Mexico
    u'150|GU', #Mexico
    u'192|OSR', #Slovenia
    u'215|ANKARA', #Turkey
    u'46|GUANGDONG', #China
    u'151|SEL', #Malaysia
    u'46|HUBEI', #China
    u'46|HUB', #China
    u'46|JIL', #China
    u'46|BEI', #China
    u'183|ST.', #Russian Federat
    u'183|MOS', #Russian Federat
    u'117|CHU', #Korea Republic
    u'106|MI', #ITALY
    u'67|BARCELONA', #Spain
    u'41|VAUD', #Switzerland
    u'150|YUCATAN', #Mexico
    u'222|NOTTINGHAMSHIRE', #United Kingdom
    u'47|CUNDINAMARCA', #Colombia
    u'101|GUJARAT', #India
    u'88|GUATEMALA', #Guatemala
    u'222|MN', #UNITED KINGDOM
    u'56|BY', #GERMANY
    u'41|GE', #SWITZERLAND
)
ALTERNATE_COUNTRIES = {
    u'CANADA': u'Canada',
    u'MALAYSIA': u'Malaysia',
    u'SINGAPORE': u'Singapore',
    u'Korea Republic': u'South Korea',
    u'Korea, Republic of': u'South Korea',
    u'Korea': u'South Korea',
    u'Russia': u'Russian Federation',
    u'US': 'United States',
    u'USA': 'United States',
    u'MEXICO': 'Mexico',
    u'ITALY': 'Italy',
    u'Hong Kong China': 'China',
    u'Russian Federat': u'Russian Federation',
    u'UNITED KINGDOM': u'United Kingdom',
    u'JAPAN': u'Japan',
    u'GERMANY': u'Germany',
}

class ZerpPartnerAddress(Zerp):
  """ Provide additional helpful support for res.partner.address records
  """

  _country_map = None
  _state_map = None

  def dict_data_normalize(self,data):
    """
    For partner addresses, we want to do some additional processing
    on the address.
    """

    country_map = self._country_map
    if not country_map:
      country_map = {}
      for country in self.get_model('res.country').search_fetch([],['name','id']):
        country_map[country.name] = country.id
        country_map[country.name.upper()] = country.id
      self._country_map = country_map

    state_map = self._state_map
    if not state_map:
      state_map = {}
      for state in self.get_model('res.country.state').search_fetch([],['code', 'country_id', 'id']):
        state_map['%d|%s' % (state.country_id.id, state.code.upper())] = state.id
      self._state_map = state_map

    # If 'country' is set, we need to convert that into a country id value
    country = ''
    if 'country' in data:
      country_name = data['country'].strip()
      country_name = ALTERNATE_COUNTRIES.get(country_name, country_name)
      if country_name:
        country_id = country_map[country_name]
      else:
        country_id = country_map['United States']
      data['country_id'] = country_id
      country = data['country']
      del data['country']

    # If 'state' is set, we need to convert that into a state id value
    state_id = False
    if 'state' in data:
      state_code = data['state'].strip()
      if country_id and state_code:
        state_key = '%d|%s' % (country_id, state_code.upper())
        if state_key not in IGNORED_STATES:
          state_id = state_map.get(state_key,False)
          if not state_id:
            import pprint
            pprint.pprint(data)
            print("WARNING:", "No state found: u'%s', #%s  " % (state_key, country))
            # raise KeyError("No state found: u'%s', #%s  " % (state_key, country))
      data['state_id'] = state_id
      del data['state']

    return super(ZerpPartnerAddress,self).dict_data_normalize(data)

  def create_contact(self,
                    row,
                    partner_id,
                    contact_name,
                    raw_row,
                    column_names
                    ):
    notes = ''
    for i in range(len(raw_row)):
      column_name = column_names[i]
      column_value = raw_row[i].strip()
      if column_name in NOTE_COLUMNS and column_value:
        if not (column_name.endswith('?') or column_name.endswith(':')):
          column_name += ':'
        notes += column_name + ' ' + column_value + '\n'

    return c.create(
      'res.partner.address',
      {
       'name': contact_name,
       'street': row['Address1'] or False,
       'street2': row['Address2'] or False,
       'phone': row['Phone1'] or False,
       'partner_id': partner_id,
       'city': row['City'] or False,
       'zip': row['ZipPostalCode'] or False,
       'notes': notes or False,
       'country_id': country_id,
       'state_id': state_id,
       'email': row['Email'] or False,
       'where_found': 'PittCon 2013'
      })


register_custom_class('res.partner.address', ZerpPartnerAddress)




class MailMessage(Zerp):
  def establish(self,rec_id,msg,reply_date,user_id,test):
    exist_msgs = self.search_fetch([
                      ('model','=','crm.helpdesk'),
                      ('res_id','=',rec_id),
                      ('body_text','=',msg),
                    ])
    if exist_msgs: return exist_msgs[0]

    if test:
      print("Would be adding an email entry for", rec_id)
      return

    message_id = self.create({
        'subject': 'Historize',
        'model': 'crm.helpdesk',
        'res_id': rec_id,
        'auto_delete': 'f',
        'subtype': 'plain',
        'state': 'received',
        'date': reply_date,
        'email_from': '',
        'body_text': msg,
        'user_id': user_id,
      })

    print("Message id:",message_id)

    return message_id

register_custom_class('mail.message', MailMessage)

class CRMHelpDesk(Zerp):
  def establish(self,
                user_rec,
                email,
                email_subject,
                email_data,
                email_date,
                notes=None,
                test=False,
                address_id=None):

    # Check to see if we can't find a user's email
    rpa_obj = self.get_model('res.partner.address')
    if address_id:
        rpa = rpa_obj.fetch_single(address_id)
    elif email:
        rpa_hits = rpa_obj.search_fetch([('email','like','%'+email+'%')]) if email else []
        if not rpa_hits:
          print("Missing:", email)
          return
        rpa = rpa_hits[0]
    else:
        print("Missing email or address_id")
        return

    # Check to see if the user's crm entry is there
    crm_hits = self.search_fetch([
                    ('name','=',email_subject),
                    ('partner_id','=',rpa.id),
                  ])
    crm = None
    if not crm_hits: # need to add it
      if test:
        print("Would have created a crm entry for",email_subject,"to",email)
        print("That would mean we would of put a message entry in as well")
        return
      else:
        crm_id = self.create({
          'name': email_subject,
          'user_id': user_rec,
          'partner_address_id': rpa,
          'partner_id': rpa.partner_id,
          'state': 'done',
          'date': email_date,
          'description': notes,
          'last_reply': email_date,
        })
        crm = self.fetch_single(crm_id)
    else:
      crm = crm_hits[0]
    crm_id = crm.id

    # Now, let's see if we've got an email registered to the user
    mm_obj = self.get_model('mail.message')
    mm_obj.establish(
      crm_id,
      email_data,
      email_date,
      user_rec,
      test
    )

register_custom_class('crm.helpdesk', CRMHelpDesk)
