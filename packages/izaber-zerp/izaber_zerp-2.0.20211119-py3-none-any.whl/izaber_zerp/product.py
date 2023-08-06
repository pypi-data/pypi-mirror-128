from __future__ import absolute_import
import pickle 

from zaber.zerp import *
import six

STATE_PREFERENCES = {
    'sellable': 1,
    'end': 2,
    'draft': 3,
    'obsolete': 4,
}

def product_sort(a,b):
    result = cmp(STATE_PREFERENCES[a['state']], STATE_PREFERENCES[b['state']])
    if result: return result
    return cmp(a['revision'], b['revision'])

class ZerpProducts(Zerp):

    def __init__(self,*args,**kwargs):
        self._product_name_cache = {}
        super(ZerpProducts,self).__init__(*args,**kwargs)

    def parse_product_name(self, product_name,state_filter=None):
        """ Parse the code into longest product found in ZERP.
            If code is T-LSM025B-S-KT04, returned array is 
            T-LSM025B-S and KT04, not T-LSM025B
        """
        if state_filter == None:
            state_filter = [('state','=','sellable')]

        # There's a lot of products to deal with so we want to cache
        # wherever possible. Still, since we'll need a different list 
        # of products for each filter
        state_filter_key = pickle.dumps(state_filter)

        # First we create a cache of all sellable product names -> ids
        if not state_filter_key in self._product_name_cache:
            new_product_name_cache = {}
            for prod in self.search_fetch(
                              state_filter,
                              ['default_code','state','revision'],
                              order_by='revision desc,sequence desc'):
                partnumber = prod.default_code
                new_product_name_cache.setdefault(partnumber,[]).append({
                    'product_id': prod.id,
                    'state': prod.state,
                    'revision': prod.revision
                  })

            for partnumber, parts in six.iteritems(new_product_name_cache.copy()):
                parts.sort(cmp=product_sort)
                new_product_name_cache[partnumber] = parts[0]['product_id']
            self._product_name_cache[state_filter_key] = new_product_name_cache

        # Then we try our best to match the partnumber to the subproducts
        # FIXME: Does this algo handle partials?
        segs = product_name.split('-')
        result = []
        i = 0
        product_name_cache = self._product_name_cache[state_filter_key]
        while i < len(segs):
            lookup = segs[i:]

            while lookup:
                search = '-'.join(lookup)
                found_id = product_name_cache.get(search,False)
                if found_id:
                    result.append(found_id)
                    i += len(lookup)
                    break
                else:
                    lookup.pop()
                    continue

            # Something didn't match. So we just bail
            if not lookup:
                return []

        return result

register_custom_class('product.product', ZerpProducts)


