<?php
/**
 * Created by PhpStorm.
 * User: lyk
 * Date: 2017/7/2 0002
 * Time: 11:24
 */
namespace Home\Controller;

use Think\Controller;

class GeopluginController extends Controller
{
    //the geoPlugin server
    var $host = 'http://www.geoplugin.net/php.gp?ip={IP}&base_currency={CURRENCY}';

    //the default base currency
    var $currency = 'USD';

    //initiate the geoPlugin vars
    var $ip = null;
    var $city = null;
    var $region = null;
    var $areaCode = null;
    var $dmaCode = null;
    var $countryCode = null;
    var $countryName = null;
    var $continentCode = null;
    var $latitude = null;
    var $longitude = null;
    var $currencyCode = null;
    var $currencySymbol = null;
    var $currencyConverter = null;

    function geoPlugin() {

    }

    function locate($ip = null) {

        global $_SERVER;

        if ( is_null( $ip ) ) {
            $ip = $_SERVER['REMOTE_ADDR'];
        }

        $host = str_replace( '{IP}', $ip, $this->host );
        $host = str_replace( '{CURRENCY}', $this->currency, $host );

        $data = array();

        $response = $this->fetch($host);

        $data = unserialize($response);

        //set the geoPlugin vars
        $this->ip = $ip;
        $this->city = $data['geoplugin_city'];
        $this->region = $data['geoplugin_region'];
        $this->areaCode = $data['geoplugin_areaCode'];
        $this->dmaCode = $data['geoplugin_dmaCode'];
        $this->countryCode = $data['geoplugin_countryCode'];
        $this->countryName = $data['geoplugin_countryName'];
        $this->continentCode = $data['geoplugin_continentCode'];
        $this->latitude = $data['geoplugin_latitude'];
        $this->longitude = $data['geoplugin_longitude'];
        $this->currencyCode = $data['geoplugin_currencyCode'];
        $this->currencySymbol = $data['geoplugin_currencySymbol'];
        $this->currencyConverter = $data['geoplugin_currencyConverter'];

    }

    function fetch($host) {

        if ( function_exists('curl_init') ) {

            //use cURL to fetch data
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $host);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_USERAGENT, 'geoPlugin PHP Class v1.0');
            $response = curl_exec($ch);
            curl_close ($ch);

        } else if ( ini_get('allow_url_fopen') ) {

            //fall back to fopen()
            $response = file_get_contents($host, 'r');

        } else {

            trigger_error ('geoPlugin class Error: Cannot retrieve data. Either compile PHP with cURL support or enable allow_url_fopen in php.ini ', E_USER_ERROR);
            return;

        }

        return $response;
    }

    function convert($amount, $float=2, $symbol=true) {

        //easily convert amounts to geolocated currency.
        if ( !is_numeric($this->currencyConverter) || $this->currencyConverter == 0 ) {
            trigger_error('geoPlugin class Notice: currencyConverter has no value.', E_USER_NOTICE);
            return $amount;
        }
        if ( !is_numeric($amount) ) {
            trigger_error ('geoPlugin class Warning: The amount passed to geoPlugin::convert is not numeric.', E_USER_WARNING);
            return $amount;
        }
        if ( $symbol === true ) {
            return $this->currencySymbol . round( ($amount * $this->currencyConverter), $float );
        } else {
            return round( ($amount * $this->currencyConverter), $float );
        }
    }

    function nearby($radius=10, $limit=null) {

        if ( !is_numeric($this->latitude) || !is_numeric($this->longitude) ) {
            trigger_error ('geoPlugin class Warning: Incorrect latitude or longitude values.', E_USER_NOTICE);
            return array( array() );
        }

        $host = "http://www.geoplugin.net/extras/nearby.gp?lat=" . $this->latitude . "&long=" . $this->longitude . "&radius={$radius}";

        if ( is_numeric($limit) )
            $host .= "&limit={$limit}";

        return unserialize( $this->fetch($host) );

    }
}