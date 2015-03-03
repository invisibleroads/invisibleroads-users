<%inherit file='invisibleroads_posts:templates/base.mako'/>
<style>
#user-link {margin-right: 1em}
</style>
<%block name="toolbar">
<form class="navbar-form navbar-right" role="toolbar" method="post" action="${request.route_path('user_logout' if user else 'user_login')}">
  <input name="target_url" value="${request.path}" type="hidden">
  <input name="csrf_token" value="${request.session.get_csrf_token()}" type="hidden">
% if user:
  <a id="user-link" href=${request.route_path('user', name=user.name)} class=navbar-link>${user.name}</a>
% endif
  <button type="submit" class="btn btn-default">${'Logout' if user else 'Login'}</button>
</form>
</%block>
${next.body()}
<%block name="head-script-inline">
var v = d.users = {};
v.assets_url = '${request.static_path("invisibleroads_users:assets/")}';
v.login_url = '${request.route_path("user_login") + "?target_url=" + request.path}';
% if user:
v.csrf_token = '${request.session.get_csrf_token()}';
v.user_id = ${user.id};
% endif
</%block>
<%block name="body-script-loaded">
<script src="${request.static_path('invisibleroads_users:assets/base.js')}"></script>
</%block>
