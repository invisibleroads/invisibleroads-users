<%!
from os.path import basename
from pyramid.settings import aslist
from titlecase import titlecase
%>
<%
settings = request.registry.settings
site_name = settings['site.name']
%>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>
% if request.path[1:]:
<%block name="title">
${titlecase(basename(request.path).replace('-', ' '))}
</%block> &middot;
% endif
${site_name}
</title>
<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css" rel="stylesheet">
<!--[if lt IE 9]>
<script src="//oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
<script src="//oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
<![endif]-->
<script>
var d = {};
var v = d.posts = {};
v.assets_url = '${request.static_path("invisibleroads_posts:assets/")}';
<%block name="head-script-inline"></%block>
</script>
</head>
<body>
<nav id="main-navbar" class="navbar navbar-default navbar-static-top navbar-inverse" role="navigation">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#main-navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="/#">${site_name}</a>
    </div>
    <div class="navbar-collapse collapse" id="main-navbar-collapse">
      <ul class="navbar-nav nav">
      % for site_section in aslist(settings.get('site.sections', [])):
        <% site_url = request.route_path(site_section.lower()) %>
        % if request.path.split('/')[1] == site_url[1:]:
        <li class="active">
        % else:
        <li>
        % endif
          <a href="${site_url}#">${site_section}</a>
        </li>
      % endfor
      </ul>
      <%block name="toolbar"></%block>
    </div>
  </div>
</nav>
<%block name="header"></%block>
<div class="container">${next.body()}</div>
<%block name="footer"></%block>
<script src="//code.jquery.com/jquery-1.11.2.min.js"></script>
<script>window.jQuery || document.write('<script src="${request.static_path("invisibleroads_posts:assets/jquery.min.js")}">\x3C/script>')</script>
<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
<script>$.fn.modal || document.write('<script src="${request.static_path("invisibleroads_posts:assets/bootstrap.min.js")}">\x3C/script>')</script>
<%block name="body-script-loaded">
<script src="${request.static_path('invisibleroads_posts:assets/base.js')}"></script>
</%block>
<script>
<%block name="body-script-inline"></%block>
</script>
</body>
</html>
