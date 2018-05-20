<?php
/**
 * Created by PhpStorm.
 * User: lyk
 * Date: 2017/6/11 0011
 * Time: 13:41
 */

namespace Home\Model;

use Think\Model;

class SelftargetModel extends Model
{

    public function getSelfTarget()
    {
        $subtypes = $this->select();
        return $subtypes;
    }

}