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

app_path('User.php');

base_path('vendor');

config_path('app.php');

database_path('UserFactory.php');

public_path('css/app.css');

resource_path('sass/app.scss');

storage_path('logs/laravel.log');

realpath(storage_path('logs/laravel.log'));

Route::get('/', [L8\EightController::class, 'index']);

Route::get('/', EightController::class);

Route::group(['namespace' => 'L8'], function () {
    Route::get('/', [\EightController::class, 'index']);
});

Route::group(['namespace' => 'L8'], function () {
    Route::get('/', [EightController::class, 'index']);
});

<x-vendor::hello />

</x-alert>

<x-forms.input/>

Route::controller(HelloController::class)->group(function () {
    Route::get('/posts/{id}', 'show');
});

Route::controller('HelloController')->group(function () {
    Route::get('/posts/{id}', 'show');
});

Route::group(['namespace' => 'Resource'], function () {
    Route::resource('photo', 'HelloController', ['only' => [
        'index', 'show'
    ]]);
});