<?php
return array(
	//'配置项'=>'配置值'
    'DB_TYPE' => 'mysql', // 数据库类型
    'DB_HOST' => 'localhost', // 服务器地址
    'DB_NAME' => 'ls', // 数据库名
    'DB_USER' => 'visitor', // 用户名
    'DB_PWD' => 'visitorpwd', // 密码
    'DB_PORT' => 3306, // 端口
    'DB_PREFIX' => '', // 数据库表前缀
    'DB_CHARSET' => 'utf8', // 字符集
    'DB_DEBUG' => TRUE, // 数据库调试模式 开启后可以记录SQL日志 3.2.3新增

    'DEFAULT_AJAX_RETURN' => 'json', // 设置默认的ajax数据返回格式
    'DEFAULT_FILTER' => 'strip_tags,addslashes,htmlspecialchars',
);