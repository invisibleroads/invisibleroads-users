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
</%block>
${next.body()}
