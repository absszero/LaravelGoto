<?php
Route::get('/', 'HelloController@index');

Route::get('/', function () {
    return view('hello_view');
});

'hello.JS';

Route::namespace('58')->group(function () {
    Route::get('/', 'FiveEightController@index');
});

Route::group(['namespace' => '52'], function () {
    Route::get('/', 'FiveTwoController@index');
});

$router->group(['namespace' => 'Lumen'], function () use ($router) {
    Route::get('/', 'LumenController@index');
});

Route::get('/', function () {
    return view('Namespace::hello_view');
});

'hello.css';
