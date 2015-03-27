<%inherit file='invisibleroads_posts:templates/base.mako'/>

<%block name="head_style_inline">
${parent.head_style_inline()}
#user-link {margin-right: 1em}
</%block>

<%block name="toolbar">
<form id="login-form" class="navbar-form navbar-right" role="toolbar" method="post" action="${request.route_path('user_logout' if user else 'user_login')}">
  <input name="target_url" value="${request.path}" type="hidden">
% if user:
  <a id="user-link" class="navbar-link" href="${request.route_path('user', name=user.name)}">${user.name}</a>
% endif
  <button type="submit" class="btn btn-default">${'Logout' if user else 'Login'}</button>
</form>
</%block>

${next.body()}

<%block name="head_script_inline">
${parent.head_script_inline()}
var v = d.users = {};
v.assets_url = '${request.static_path("invisibleroads_users:assets/")}';
v.login_url = '${request.route_path("user_login") + "?target_url=" + request.path}';
% if user:
v.csrf_token = '${request.session.get_csrf_token()}';
v.user_id = ${user.id};
% endif
</%block>

<%block name="body_script_loaded">
<script src="${request.static_path('invisibleroads_users:assets/base.js')}"></script>
</%block>