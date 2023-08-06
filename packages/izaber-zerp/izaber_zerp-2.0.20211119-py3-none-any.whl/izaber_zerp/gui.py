from __future__ import absolute_import
from zaber.zerp import *

class ZerpMenuItem(ZerpRecord):
  def execute(self,*args,**kwargs):
    """ Attempt to execute this menu item
    """
    try:
      action = self.action
      if not action: raise Exception('Menu item %s does not have an action' % self)

      model, res_id = action.split(',')

      if model == 'ir.actions.act_window':
        context = {}
        action_rec = self.zerp.get_model(model).fetch_single(res_id)
        return self.zerp.client.execute(
          action_rec.res_model,
          'fields_view_get',
          action_rec.search_view_id[0],
          'search',
          { 'active_ids': [self.id], 
            'active_model': 'ir.ui.menu', 
            'active_id': self.id, }
        )

      elif model == 'ir.actions.server':
        return self.zerp.client.execute(
          model,
          'run',
          [int(res_id)],
          { 'active_ids': [self.id], 
            'active_model': 'ir.ui.menu', 
            'active_id': self.id, }
        )

      elif model == 'ir.actions.wizard':
        action_rec = self.zerp.get_model(model).fetch_single(res_id)
        result = self.zerp.client.wizard_create(action_rec.wiz_name)
        return {
          'session_id': result
        }

      else:
        raise Exception('Do not know how to handle menuitem %s' % self)

    except Exception as ex:
      return {
        'error': str(ex),
        'exception': ex
      }

class ZerpMenu(Zerp):
  """ Provide additional helpful support for menu items
  """
  def menuitems(self,parent_id=False):
    """ Return a lookup structure for menu items (at root base)
    """
    if parent_id: parent_id = int(parent_id)
    if not parent_id: parent_id = False
    menuitem_hits = self.search_fetch(
                        [('parent_id','=',parent_id)]
                        )
    return menuitem_hits

  def dump_tree(self,dump_func=None,depth=0,indent="    ",parent_id=False):
    """ Recusively build a tree of all the menu items. TODO: this is not
        the fastest way of building the tree. Unfortunately because of
        the latency in each request, it's actually quite slow. Better to
        do a single query then build from that.
    """
    if dump_func == None:
      dump_func = lambda m: "{id}: {name} <{action}>\n".format(**m._rec)
    menuitems = self.menuitems(parent_id)
    out = ""
    for menuitem in menuitems:
      out += indent*depth + dump_func(menuitem)
      out += self.dump_tree(dump_func,depth+1,indent,menuitem.id)
    return out

  def record_instantiate(self,rec,new_record=False):
    """ Override to allow the hooking of special actions to the ZerpMenuItems
    """
    return ZerpMenuItem(
      zerp=self,
      model_metadata=self._model_metadata,
      rec=rec,
      new_record=new_record
    )


register_custom_class('ir.ui.menu', ZerpMenu)
