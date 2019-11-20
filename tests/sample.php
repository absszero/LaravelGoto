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

Route::group(['namespace' => 'Abc'], function () {
    Route::get('/', '\Absolute\IndexController@index')->name('index');
});

Config::get('app.timezone');

Config::set(   'app.timezone', 'UTC');

config('app');

config('app.timezone');

config(     ['app.timezone' => 'UTC']);

env(   'APP_DEBUG', false);

__('messages.welcome');

@lang('messages.welcome');

trans('messages.welcome');

trans_choice('messages.apples', 10);

trans('package::messages');

'./../../hello.css'

config(['app.timezone' => config('app.tz')]);

view('package::hello_view');