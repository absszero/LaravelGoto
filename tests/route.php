<?php
Route::get('/', 'HelloController@index')

Route::get('/', function () {
    return view('hello_view');
});

'hello.js'
