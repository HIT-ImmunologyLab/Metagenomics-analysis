<?php
namespace Home\Controller;


class IndexController extends BaseController
{

    // *********************************************************
    // zero --- home
    // *********************************************************

    public function index()
    {
        $data = $this->getRegion();
        if ( $data ) {
            // 数据库操作
            $ar = M("Access_records");
            $retArr = $ar->where("ip = '".$data['ip']."'")->select();
            if ( count($retArr) ) {
                $now = time();
                for ( $i=0; $i<count($retArr); $i++ ) {
                    if ( intval($retArr[$i]['last_access'])<($now-3600) ) {
                        $ar->last_access = $now;
                        $ar->num = $retArr[$i]['num'] + 1;
                        $ar->where("id = ".$retArr[$i]['id'])->save();
                    }
                }
            } else {
                $data['last_access'] = time();
                $data['num'] = 1;
                $ar->filter("strip_tags")->add($data);
            }
        }
        //  end
        $this->display("Crispr/prediction");
    }

    public function getRegion()
    {
        $ip = $this->getIP();
        if ( $ip ) {

        //var_dump($ip);

//        require_once('./admin/files/geoplugin.php');

//        $geoplugin = new geoPlugin();
            $geoplugin = A("Geoplugin");
        // If we wanted to change the base currency, we would uncomment the following line
        // $geoplugin->currency = 'EUR';

            $geoplugin->locate($ip);

//        echo "Geolocation results for {$geoplugin->ip}: <br />\n".
//            "City: {$geoplugin->city} <br />\n".
//            "Region: {$geoplugin->region} <br />\n".
//            "Area Code: {$geoplugin->areaCode} <br />\n".
//            "DMA Code: {$geoplugin->dmaCode} <br />\n".
//            "Country Name: {$geoplugin->countryName} <br />\n".
//            "Country Code: {$geoplugin->countryCode} <br />\n".
//            "Longitude: {$geoplugin->longitude} <br />\n".
//            "Latitude: {$geoplugin->latitude} <br />\n".
//            "Currency Code: {$geoplugin->currencyCode} <br />\n".
//            "Currency Symbol: {$geoplugin->currencySymbol} <br />\n".
//            "Exchange Rate: {$geoplugin->currencyConverter} <br />\n";
            $data['ip'] = $ip;
            $data['country'] = $geoplugin->countryName;
            $data['country_code'] = $geoplugin->countryCode;
            $data['region'] = $geoplugin->region;
            $data['city'] = $geoplugin->city;
            return $data;

        } else {
            return null;
        }
    }

//    public function test() {
//        $data = $this->getRegion();
//        var_dump($data);
//        // 数据库操作
//        $ar = M("Access_records");
//        $retArr = $ar->where("ip = '".$data['ip']."'")->select();
//        var_dump($retArr);
//        var_dump(count($retArr));
//        if ( count($retArr) ) {
//            $now = time();
//            var_dump($now);
//            for ( $i=0; $i<count($retArr); $i++ ) {
//                if ( intval($retArr[$i]['last_access'])<($now-3600) ) {
//                    $ar->last_access = $now;
//                    $ar->num = $retArr[$i]['num'] + 1;
//                    $ar->where("id = ".$retArr[$i]['id'])->save();
//                }
//            }
//        } else {
//            $data['last_access'] = time();
//            $data['num'] = 1;
//            $ar->filter("strip_tags")->add($data);
//        }
//        //  end
//    }

    public function getIP() {
        if ($_SERVER['HTTP_CLIENT_IP']&&!empty($_SERVER['HTTP_CLIENT_IP'])&&strcasecmp($_SERVER['HTTP_CLIENT_IP'], 'unknown')) {
            $ip = $_SERVER['HTTP_CLIENT_IP'];
        } elseif ($_SERVER['HTTP_X_FORWARDED_FOR']&&!empty($_SERVER['HTTP_X_FORWARDED_FOR'])&&strcasecmp($_SERVER['HTTP_X_FORWARDED_FOR'], 'unknown'))
        {
            $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
        } elseif($_SERVER['REMOTE_ADDR']&&!empty($_SERVER['REMOTE_ADDR'])&&strcasecmp($_SERVER['REMOTE_ADDR'], 'unknown')) {
            $ip = $_SERVER['REMOTE_ADDR'];
        } else {
            $ip = null;
        }

        if ( false !== strpos($ip, ',') ) {
            $ip = reset(explode(',', $ip));
        }
        return $ip;
    }

    /**
     * 访问量查看
     * @return [type] [description]
     */
    public function location() {
        $this->display();
    }


    // *********************************************************
    // three --- classification
    // *********************************************************

    public function classification() {
//        $classification = I('get.classification');
        // $colorTable = $this->getColorTable();
        // $this->assign("ct", $colorTable);
//        if ( $classification ) {
//            $data['visible'] = "a-show";
//            $data['classification'] = $classification;
//            $st = D("Subtypes");
//            $data['data'] = $st->getSubtypes($classification);
//            if ( !$data['data'] ) {
//                $data['data'] = false;
//                $data['msg'] = "此类别没有数据！";
//            }
//        } else {
            $data['visible'] = "a-hide";
            $data['classification'] = null;
            $data['data'] = null;
//        }
        $this->assign("data", $data);
        $this->display();
    }

    public function architectures() {
        $colorTable = $this->getColorTable();
        $this->assign("ct", $colorTable);
        $this->display();
    }

    //获取某一种类的信息
    public function getType() {
        if ( IS_POST ) {
            $type = I('post.type');
            if ( $type ) {
                $st = D("Subtypes");
                $data['data'] = $st->getSubtypes($type);
                $this->ajaxReturn($data);
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }


    // 获取 color 文件中的数据
    public function getColorTable() {
        $filename = "./admin/files/table3";
//        $file = fopen($filename, "r") or die("Unable to open table");
        $file = file_get_contents("./admin/files/table3");
        $arr = explode("\n", $file);
        $data = array();
        for ( $i=0; $i<count($arr); $i++ ) {
            $arr2 = explode("\t", $arr[$i]);
            array_push($data, $arr2);
        }
//        while ( !feof($file) ) {
//            $content = fgets($file);
//            $arr = explode("\t", $content);
//            array_push($data, $arr);
//        }
        return $data;
    }


    // *********************************************************
    // four --- self-target
    // *********************************************************

    public function selfTarget()
    {
        $st = D("Selftarget");
        $arr = $st->field("count(*) as allNum")->select();
        $this->assign("allNum", ceil($arr[0]['allnum']/1000)+1);
        $this->display();
    }

//    public function getSelfTargetInfo() {
//        if ( IS_GET ) {
//            $st = D("Selftarget");
//            $arr['data'] = $st->getSelfTarget();
//            $this->ajaxReturn($arr);
//        } else {
//            $this->display("Common/404");
//        }
//    }

    public function getSelfTargetInfo2() {
        if ( IS_GET ) {
            $st = D("Selftarget2");
            $arr['data'] = $st->select();
            $this->ajaxReturn($arr);
        } else {
            $this->display("Common/404");
        }
    }

    public function getSelfTargetInfo() {
        if ( IS_POST ) {
            $limit = I('post.limit');
            $st = D("Selftarget");
            $arr['data'] = $st->limit(($limit-1)*1000 . ", " . 1000)->select();
            $this->ajaxReturn($arr);
        } else {
            $this->display("Common/404");
        }
    }

   	public function getBothRefseq() {
   		if ( IS_GET ) {
   			$brs = D("Bothrefseq");
   			$arr['data'] = $brs->order('source desc')->select();
   			// printf_r($arr);
   			$this->ajaxReturn($arr);
   		} else {
   			$this->display("Common/404");
   		}
   	}


    // *********************************************************
    // five --- interaction
    // *********************************************************

    // 交互页面
    public function interaction()
    {
        $pg = M("Prophage");
        $arr = $pg->field("count(*) as allnum")->select();
        $this->assign("allNum", ceil($arr[0]['allnum']/1000)+1);
        $this->display();
    }

    public function getInteractionInfo1() {
        if ( IS_GET ) {
            $ir = D("Interaction");
            $data['data'] = $ir->getSpecieInteraction();
//            var_dump($data);
          $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    public function getNcbiInfo() {
        if ( IS_GET ) {
            $ncbi = M("Ncbi");
            $data['data'] = $ncbi->field("phage_name, refseq_id, bacteria_organism, bacteria_taxonomy_level")->select();
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

//    public function getProphageInfo() {
//        if ( IS_GET ) {
//            $pg = M("Prophage");
//            //$data['data'] = $pg->field("phage_name, refseq_id, bacteria_organism, bacteria_taxonomy_level")->select();
////            $data['data'] = M()->table(array("prophage"=>"pg", "prophage_info"=>"pg2"))->field("pg.bacteria_id, pg.region_id, pg.completeness, pg.region_position, pg.most_common_phage, pg2.description")
//            $data['data'] = $pg->join("left join prophage_info ON prophage.bacteria_id = prophage_info.bid")->select();
//            $this->ajaxReturn($data);
//        } else {
//            $this->display("Common/404");
//        }
//    }

    public function getProphageInfo() {
        if ( IS_POST ) {
            $limit = I('post.limit');
            $pg = M("Prophage");
//            $data['data'] = $pg->join("left join prophage_info ON prophage.bacteria_id = prophage_info.bid")->limit(($limit-1)*1000 . ", " . 1000)->select();
            $data['data'] = $pg->where("id > ".(($limit-1)*1000)." and id<= " . ($limit*1000))->join("left join prophage_info ON prophage.bacteria_id = prophage_info.bid")->select();
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    public function getInteractionInfo2() {
        if ( IS_GET ) {
            $ir = D("Interaction");
            $data['data'] = $ir->getGenusInteraction();
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    // 交互记录的详情
    public function getDetailInteraction() {
        if ( IS_POST ) {
            $kind = I('post.kind');
            $value = I('post.value');
            $ir = D("Interaction");
            //$details['data'] = $ir->getDetails($kind, $value);
            //$details['data'] = M()->table(array('Interaction'=>'i','ncbi'=>'n'))->field('i.id, i.bacteria_id, i.bacteria_name, i.specie, i.genus, i.phage_id, i.phage_name, n.bacteria_organism')->where($kind. " = '" . $value . "' AND i.phage_id = n.refseq_id")->select();
//            $details['data'] = $ir->where($kind. " = '" . $value . "'")->select();
            $data = $ir->where($kind. " = '" . $value . "'")->select();

            $ncbi = M("Ncbi");
            if ( count($data) ) {
                for ( $i=0; $i<count($data); $i++ ) {
                    $details['data'][$i]['id'] = $data[$i]['id'];
                    $details['data'][$i]['bacteria_id'] = $data[$i]['bacteria_id'];
                    $details['data'][$i]['bacteria_name'] = $data[$i]['bacteria_name'];
                    $details['data'][$i]['specie'] = $data[$i]['specie'];
                    $details['data'][$i]['genus'] = $data[$i]['genus'];
                    $details['data'][$i]['phage_id'] = $data[$i]['phage_id'];
                    $details['data'][$i]['phage_name'] = $data[$i]['phage_name'];
                    $details['data'][$i]['spacer_id'] = $data[$i]['spacer_id'];
                    $details['data'][$i]['missmatch'] = $data[$i]['missmatch'];
                    $details['data'][$i]['flag'] = $data[$i]['flag'];
                    $details['data'][$i]['bacteria_organism'] = "";
                    $arr = $ncbi->field("bacteria_organism")->where("refseq_id = '" . $data[$i]['phage_id'] . "'")->select();
                    $details['data'][$i]['bacteria_organism'] = $arr[0]['bacteria_organism'];
                }
            }

            if ( $details ) {
                $this->ajaxReturn($details);
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 获取spacer_sequence, hit_sequence, long_hit_sequence之间的联系
    public function getSequenceCompare() {
        if ( IS_POST ) {
            $b_id = I('post.b_id');
            $p_id = I('post.p_id');
            $s_id = I('post.s_id');
            $sq = D("Sequence");
            $data = $sq->where("bac_id = '" . $b_id . "' and phage_id = '" . $p_id . "' and spacer_id = '" . $s_id . "'")->select();
            if ( $data[0]['hit_sequence'] && $data[0]['long_hit_sequence'] ) {
                $start = strpos($data[0]['long_hit_sequence'], $data[0]['hit_sequence']);
                $str = "";
                for ($i=0; $i<$start; $i++ ) {
                    $str .= " ";
                }
                $data[0]['hit_sequence'] = $str . $data[0]['hit_sequence'];
                str_repeat($data[0]['hit_sequence'], "<font color='#f00'>".$data[0]['hit_sequence']."</font>", $data[0]['long_hit_sequence']);
            }
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    // 获取生产的蛋白的信息
    public function getCreateProtein() {
        if ( IS_POST ) {
            $b_id = I('post.b_id');
            $p_id = I('post.p_id');
            $s_id = I('post.s_id');
            $hp = D("hitprotein");
            $data = $hp->field("protein_id, protein_product")->where("bac_id = '" . $b_id . "' and phage_id = '" . $p_id . "' and spacer_id = '" . $s_id . "'")->select();
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    // *********************************************************
    // six --- anti-crispr
    // *********************************************************


    //
    public function antiCrispr()
    {
        $this->display();
    }

    // 获取初始table数据
    public function getAntiCrisprInfo() {
        if ( IS_GET ) {
            $ac = D("Anticrispr");
            $arr['data'] = $ac->getAnticrispr();
            $this->ajaxReturn($arr);
        } else {
            $this->display("Common/404");
        }
    }

    // 获取所有同源的细菌的数据
    public function handleAntiCrispr()
    {
        if ( IS_POST ) {
            $id = I('post.id');
            if ( $id ) {
                $data = $this->getAntiData($id);
                $this->ajaxReturn($data);
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    public function getAntiData($id) {
//        $id = "ACD38920.1";
        $hp = M("homologyprotein");
        $pd = M("proteindomain");

        $data = array();

        // 获取所有的同源蛋白
        $hpData = $hp->field("proteinid, geneid, genename")->where("antiproteinId = '" . $id . "'")->select();


        // 获取所有的同源蛋白的同样基因的
        $i = 0;
        if ( count($hpData) ) {
            for ( $p=0; $p<count($hpData); $p++ ) {
                $pdDataBefore = $pd->where("geneid = '" . $hpData[$p]['geneid'] . "' AND proteinId < '". $hpData[$p]['proteinid'] . "'")->order("proteinId desc")->select();
                $data[$i]['before'] = $pdDataBefore;
                $pdDataAfter = $pd->where("geneid = '" . $hpData[$p]['geneid'] . "' AND proteinId > '". $hpData[$p]['proteinid'] . "'")->order("proteinId asc")->select();
                // 给homologyprotein添加 proteindomain中的position信息
                $hpDataOther = $pd->where("geneid = '" . $hpData[$p]['geneid'] . "' AND proteinId = '". $hpData[$p]['proteinid'] . "'")->select();
                $data[$i]['after'] = $pdDataAfter;
                if ( !empty($hpDataOther) ) {
                    $hpData[$p]['position'] = $hpDataOther[0]['position'];
                }
                $data[$i]['mid'] = $hpData[$p];
                $i ++;
            }
        }

//        var_dump($data);

        $dat = array();
        $hpData2 = array();

        // 去掉空值项
        for ( $i=0; $i<count($data); $i++ ) {
            if ( !count($data[$i]) ) {
                unset($data[$i]);
                unset($hpData[$i]);
            } else {
                array_push($dat, $data[$i]);
                array_push($hpData2, $hpData[$i]);
            }
        }


        $result = array();

        if ( count($dat) ) {
            for ( $i=0; $i<count($dat); $i++ ) {
                $arr['before'] = $this->getMaxData($dat[$i]['before'], 5);
                $arr['after'] = $this->getMaxData($dat[$i]['after'], 5);
                $arr['mid'] = $dat[$i]['mid'];
                array_push($result, $arr);
            }
        }

        return $result;
    }

    // 获取数组重复项最大的值 -- 有重复项，去最大值，其他舍弃
    // 要求：$data 中一定要有数据
//    public function getMaxData($data, $limit) {
//        var_dump($limit);
//        $count = 0;
//        if ( count($data) ) {
//            $k = 0;
//            $result = array();
//            $j = 0;
//            while($j<count($data) && $count<$limit) {
//                if ( $data[$j]['evalue']=="NULL" || $data[$j]['identy']=="NULL" ) {
//                    if ( $k==$j ) {
////                        array_push($result, $data[$k]);
//                        array_push($result, array($data[$k]['proteinid'], $data[$k]['proteindomain'], $data[$k]['position']));
//                        $count ++;
//                        $j ++;
//                        $k = $j;
//                    } else {
////                        array_push($result, $data[$k]);
//                        array_push($result, array($data[$k]['proteinid'], $data[$k]['proteindomain'], $data[$k]['position']));
//                        $count ++;
////                        array_push($result, $data[$j]);
//                        if ( $count<$limit ) {
//                            array_push($result, array($data[$j]['proteinid'], $data[$j]['proteindomain'], $data[$j]['position']));
//                            $count ++;
//                            $j ++;
//                            $k = $j;
//                        } else {
//                            break;
//                        }
//
//                    }
//                } else {
//                    if ( $data[$j]['proteinid']==$data[$k]['proteinid'] ) {
//                        if ( $data[$j]['identy']>$data[$k]['identy'] ) {
//                            $k = $j;
//                        } else if ( $data[$j]['identy']>$data[$k]['identy'] ) {
//                            if ( ($data[$j]['evalue']+0)>($data[$k]['evalue']+0) ) {
//                                $k = $j;
//                            }
//                        }
//                    } else {
//                        array_push($result, array($data[$k]['proteinid'], $data[$k]['proteindomain'], $data[$k]['position']));
//                        $count ++;
//                        $k = $j;
//                    }
//                }
//                $j ++;
//            }
//            if ( $count<($limit-1) ) {
//                var_dump("::::".$count);
//                if ( $k<count($data) ) {
//                    array_push($result, array($data[$k]['proteinid'], $data[$k]['proteindomain'], $data[$k]['position']));
//                    $count ++;
//                }
//            }
//            var_dump($count);
//            return $result;
//        } else {
//            return null;
//        }
//    }



    public function getMaxData($data, $limit) {
        $count = 0;
        if ( count($data) ) {
            $k = 0;
            $result = array();
            $j = 0;
            while($j<count($data) && $count<$limit) {
                if ( $data[$j]['evalue']=="NULL" || $data[$j]['identy']=="NULL" ) {
                    if ( $k==$j ) {
                        array_push($result, array($data[$k]['proteinid'], $data[$k]['proteindomain'], $data[$k]['position']));
                        $count ++;
                    } else {
                        if ( $data[$k]['proteinid']!=$data[$j]['proteinid'] ) {
                            $k = $j;
                            array_push($result, array($data[$k]['proteinid'], $data[$k]['proteindomain'], $data[$k]['position']));
                            $count++;
                        }
                    }
                } else {
                    if ( $k==$j ) {
                        array_push($result, array($data[$k]['proteinid'], $data[$k]['proteindomain'], $data[$k]['position']));
                        $count ++;
                    } else {
                        if ( $data[$j]['proteinid']==$data[$k]['proteinid'] ) {
                            if ( $data[$j]['identy']>$data[$k]['identy'] ) {
                                $k = $j;
                            } else if ( $data[$j]['identy']==$data[$k]['identy'] ) {
                                if ( ($data[$j]['evalue']+0)>($data[$k]['evalue']+0) ) {
                                    $k = $j;
                                }
                            }
                        } else {
                            $k = $j;
                            array_push($result, array($data[$k]['proteinid'], $data[$k]['proteindomain'], $data[$k]['position']));
                            $count ++;
                        }
                    }
                }
                $j ++;
            }
            return $result;
        } else {
            return null;
        }
    }

    
    // *********************************************************
    // seeven --- help
    // *********************************************************

     public function help()
    {
        $this->display();
    }
}
