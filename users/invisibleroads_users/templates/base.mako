<%! script_url = '/_/invisibleroads-users/base' %>
<%inherit file='invisibleroads_posts:templates/base.mako'/>
<style>
#main-navbar-collapse a {margin-right: 1em}
</style>
<%block name="toolbar">
<%
login_url = request.route_path('user_login') + '?target_url=' + request.path
logout_url = request.route_path('user_logout') + '?target_url=' + request.path
%>
<form class="navbar-form navbar-right" role=toolbar method=post action='${logout_url if user else login_url}'>
% if user:
  ## <a href=${request.route_path('user')} class=navbar-link>${user.name}</a>
  <a class=navbar-link>${user.name}</a>
% endif
  <button type="submit" class="btn btn-default">${'Logout' if user else 'Login'}</button>
</form>
<script>
var v = d.users = {}
v.assets_url = '${request.static_path("invisibleroads_users:assets/")}';
v.login_url = '${login_url}';
% if user:
v.csrf_token = '${request.session.get_csrf_token()}';
v.user_id = ${user.id};
% endif
</script>
</%block>
${next.body()}
