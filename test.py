from AWhereCall import AWhereCall

key = 'lpGunnkiij1439P1f3xFNer9GA3aL1eI'
secret = '61WbUcQiStz5mSMv'
field = 'gus_dc'

y = AWhereCall(key, secret)

#fields = y.get_fields()
#print fields

#resp = y.create_field(38.9, 77, 'gus_dc', 'dc')

#print resp


out = y.get_observations(field)

print out
print out['observations'][0]['location']['latitude']

'''
flat = y.flatten_observations(out)

print flat
'''