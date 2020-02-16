<nav>
    <input id="search_input" onkeyup="search_func()" type="text" placeholder="search...">
	<ul id="search_items">
		% for item in md:
		<li><a href="/{{item.pretty_filename}}">{{item.url_path}}</a></li>
		% end 
	</ul>
</nav>
<div class="markdown-body">
{{!info}}
</div>
