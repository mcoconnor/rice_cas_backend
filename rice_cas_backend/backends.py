import ldap

from django_cas.backends import CASBackend
from django.conf import settings


def create_cas_connection(
    host_name=getattr(settings, 'LDAP_SERVER', 'ldap://directory.rice.edu'),
    user=settings.LDAP_USER,
    password=settings.LDAP_PASSWORD):
    """
    Establish ldap connection to Rice University CAS service
    """
    connection = ldap.initialize(host_name)
    connection.protocol_version = ldap.VERSION3
    try:
        connection.simple_bind(user, password)
    except:
        connection.simple_bind('','')
    return connection

def get_cas_userdata(lookup_value, lookup_key="uid", connection=None,
				 user_base_dn='ou=People,dc=rice,dc=edu',
				 users_filter='(objectclass=person)(riceuserstatus=active)',
				 retrieve=[
					 'uid',
					 'givenName',
					 'sn',
					 'mail',
					 'eduPersonPrimaryAffiliation',
					 'riceClass',
					 'riceID',
					 'riceDOB',
					 'riceGender',
					 'riceOrg',
					 'riceCollege',
					 'riceCourse',
					 'riceDisplayOption']):
	"""
	Lookup for user attributes
	"""    
	if not connection:
		connection = create_cas_connection()

	query = '(&%s(%s=%s))' % (users_filter, lookup_key, lookup_value)

	try:
		ldap_results = connection.search_s(user_base_dn, ldap.SCOPE_SUBTREE, query, retrieve)
		if len(ldap_results) == 0:
			return None
		ldap_result = ldap_results[0][1]

		rice_user_data = {}
		rice_user_data['username'] = ldap_result.get('uid', [lookup_value if lookup_key =='uid' else ''])[0]
		rice_user_data['first_name'] = ldap_result.get('givenName', [''])[0]
		rice_user_data['last_name'] = ldap_result.get('sn', [''])[0]
		rice_user_data['email'] = ldap_result.get('mail', [''])[0]
		rice_user_data['affiliation'] = ldap_result.get('eduPersonPrimaryAffiliation', [''])[0]
		rice_user_data['classification'] = ldap_result.get('riceClass', [''])[0]
		rice_user_data['rice_id'] = ldap_result.get('riceID', [''])[0]
		rice_user_data['date_of_birth'] = ldap_result.get('riceDOB', [''])[0]
		rice_user_data['gender'] = ldap_result.get('riceGender', [''])[0]
		rice_user_data['rice_org'] = ldap_result.get('riceOrg', [''])[0]
		rice_user_data['college'] = ldap_result.get('riceCollege', [''])[0]
		rice_user_data['course'] = ldap_result.get('riceCourse', [''])[0]
		rice_user_data['display_option'] = ldap_result.get('riceDisplayOption', [''])[0]
		return rice_user_data
	except:
		return None

class RiceCASBackend(CASBackend):
    """CAS authentication backend with LDAP user details lookup"""
	
    def authenticate(self, ticket, service):
        """Authenticates CAS ticket and retrieves user data"""

        user = super(RiceCASBackend, self).authenticate(
            ticket, service)

        #if the user data hasn't already been populated, do so now	
        if user and not user.last_name:
            try:
                connection = create_cas_connection()
                rice_user_data = get_cas_userdata(user.username, connection=connection)
                print rice_user_data
            except Exception, e:
                print e
                rice_user_data = {}

            user.first_name = rice_user_data.get('first_name','')
            user.last_name = rice_user_data.get('last_name','')
            user.email = rice_user_data.get('email','')
            user.save()
            
        return user
    
