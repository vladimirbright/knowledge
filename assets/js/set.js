// ----------------------------------------------------------------------------
// markItUp!
// ----------------------------------------------------------------------------
// Copyright (C) 2008 Jay Salvat
// http://markitup.jaysalvat.com/
// ----------------------------------------------------------------------------
// BBCode tags example
// http://en.wikipedia.org/wiki/Bbcode
// ----------------------------------------------------------------------------
// Feel free to add more tags
// ----------------------------------------------------------------------------
mySettings = {
	previewParserPath:	'', // path to your BBCode parser
	markupSet: [
		{name:'python', openWith:'[code=py]', closeWith:'[/code]'},
		{name:'php', openWith:'[code=php]<?php', closeWith:'?>[/code]'},
		{name:'bash', openWith:'[code=bash]', closeWith:'[/code]'},
		{name:'perl', openWith:'[code=perl]', closeWith:'[/code]'},
		{name:'html', openWith:'[code=html]', closeWith:'[/code]'},
		{name:'css', openWith:'[code=css]', closeWith:'[/code]'},
		{name:'javascript', openWith:'[code=js]', closeWith:'[/code]'}
	]
}
