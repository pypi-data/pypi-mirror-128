## -*- coding: utf-8; -*-
<%inherit file="/batch/index.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if generic_template_url and master.has_perm('create'):
      <li>${h.link_to("Download Generic Template", generic_template_url)}</li>
  % endif
  % if h.route_exists(request, 'vendors') and request.has_perm('vendors.list'):
      <li>${h.link_to("View Vendors", url('vendors'))}</li>
  % endif
</%def>

${parent.body()}
