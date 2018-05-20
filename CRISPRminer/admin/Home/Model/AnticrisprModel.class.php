<?php
/**
 * Created by PhpStorm.
 * User: lyk
 * Date: 2017/6/11 0011
 * Time: 14:08
 */

namespace Home\Model;

use Think\Model;

class AnticrisprModel extends Model
{

    public function getAnticrispr($type)
    {
        $subtypes = $this->order("antiproteinId asc")->select();
        return $subtypes;
    }

}