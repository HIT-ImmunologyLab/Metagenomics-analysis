<?php
/**
 * Created by PhpStorm.
 * User: lyk
 * Date: 2017/6/11 0011
 * Time: 0:55
 */

namespace Home\Model;

use Think\Model;

class SubtypesModel extends Model
{

    public function getSubtypes($type)
    {
        $subtypes = $this->where("classification like '". $type ."%'")->select();
        if ( !empty($subtypes) ) {
        	for ( $i=0; $i<count($subtypes); $i++ ) {
        		$subtypes[$i]["cas_locus"] = trim(trim($subtypes[$i]["cas_locus"]), ",");
        	}
        }
        return $subtypes;
    }

}