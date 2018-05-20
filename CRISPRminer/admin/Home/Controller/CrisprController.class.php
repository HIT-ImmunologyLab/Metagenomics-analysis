<?php
/**
 * Created by PhpStorm.
 * User: lyk
 * Date: 2017/6/14 0014
 * Time: 12:59
 */

namespace Home\Controller;

class CrisprController extends BaseController
{

    private $limitNumber = 100;
    private $filePath = "/zrom/jobs/bacteria/";
    private $folder;


    // *********************************************************
    // one --- prediction
    // *********************************************************

    public function prediction()
    {
        $this->display();
    }

    // 处理文件上传
    public function handleUpload()
    {
        if ( IS_POST ) {
            if (0 || ((isset($_FILES['ls']['tmp_name'])) && ($_FILES['ls']['tmp_name'] != ''))) {
                //==处理文件上传=====
                $folder = time();
                $uploadPath = '/zrom/upload/'. $folder . '/';
                $isSuccess = mkdir('/zrom/upload/'. $folder);
                if ( $isSuccess ) {
                    $cmd = system("chmod 0777 /zrom/upload/".$folder ,$ret);
                    $upload = new \Think\Upload(); // 实例化上传类
                    $upload->maxSize = 10485760; // 设置附件上传大小
                    $upload->rootPath = $uploadPath; // 设置附件上传根目录
                    $upload->savePath = ''; // 设置附件上传（子）目录
                    $upload->autoSub = false;
                    // 上传文件
                    $info = $upload->upload();
                    if (!$info) {
                        // 上传错误提示错误信息
                        $this->error($upload->getError());
                        return false;
                    }
                    $savename = $info['ls']['savename'];
                    $cmd = system("chmod 0777 /zrom/upload/".$folder."/".$savename ,$ret);

                    $cmd = system("/zrom/z-tools/bin/call_load ".$uploadPath.$savename, $ret);
                    if ( !$ret ) {
                        $this->filePath = $uploadPath.$savename;
                        $pid = $this->getIDByFna($this->filePath);
                        // 将文件名称插入数据库
                        // =================================
                        $fileTable = M("Filename");
                        $tableArr['name'] = $this->filePath;
                        $daa = $fileTable->filter("strip_tags")->add($tableArr);
                        if ( $daa ) {
                            // ========================
                            // 获得该文件件名的ID
                            $tableSelectArr = $fileTable->field("id")->where("name = '".$this->filePath."'")->select();
                            $fileId = $tableSelectArr[0]['id'];
                            // ============================
                            $file_name = ".stat";
                            $fp = $this->filePath ."". $file_name;
                            $flag = 1;
                            while ( $flag ) {
                                $text = file_get_contents($fp);
                                if ( strstr($text, "jobs all done!") ) {
                                    $flag = 0;
                                }
                            }
//                            $this->assign("fileId", $fileId);
//                            $this->assign("pid", $pid);
//                            $this->display();
                            $pid = str_replace(".", "_", $pid);
                            $this->redirect("Crispr/predictionResult", array("fileId"=>$fileId, "pid"=>$pid));
                        } else {
                            $this->error("There is a error exists!");
                        }
                    } else {
                        $this->error("The program running failed!");
                    }

                } else {
                    $this->error("make file failed!");
                }
            }
        } else {
            $this->error("upload failed!");
        }
    }

    // 负责展示预测处理后的数据
    public function predictionResult() {
        $this->display();
    }

    public function handlePredictionExample() {
        // $pid = "NC_017545";
        $pid = "NC_008532";
        // $this->countFilePath($pid);
        // $fileId = 99;
        // $this->redirect("Crispr/searchResult", array("fileId"=>$fileId, "pid"=>$pid));
        $this->assign('pid', $pid);
        $this->display("Crispr/searchResult");
        // $content = file_get_contents($this->filePath . ".fna");
        // echo $content;
        // $this->ajaxReturn(json_encode($content));
    }

    public function handlePredictionExample2() {
        // $pid = "NC_017545";
        // $this->countFilePath($pid);
        $path = "/var/www/html/CRISPRminer/Public/file/Example_sequence.fasta";
        // $fileId = 58;
        // $this->redirect("Crispr/predictionResult", array("fileId"=>$fileId, "pid"=>$pid));
        // $content = file_get_contents($this->filePath . ".fna");
        $content = file_get_contents($path);
        echo $content;
        // $this->ajaxReturn(json_encode($content));
    }

    // 获取selftarget数据
    public function getPredictionSelftarget() {
        if ( IS_POST ) {
            $pid = I("post.fileId"); // 数据库里的文件路径名对应的id
            $fileTable = M("filename"); // 存储id和文件路径所用的表
            $arr = $fileTable->where("id = ".$pid)->select(); // 根据id寻找出表中对应的文件路径
            $arr2 = explode("/", $arr[0]['name']);
            $num = count($arr2);
            $result = $arr2[$num-1]; // 获取具体的文件名

            // echo $result;

            // $fasn = $arr[0]['name']."".".fasn";
            $fasn = $arr[0]['name']."".".fasn";
            // echo $fasn;

            $data = array();
            $proxy = array();

            if ( file_exists($fasn) ) {
                // $file = fopen($fasn, "r") or die("unable open the file --- getPredictionSelftarget");
                $content = file_get_contents($fasn);
                if ( $content ) {
                    $contentArr = explode("\n", $content);
                    if ( count($contentArr) ) {
                        for ( $i=0; $i<count($contentArr); $i++ ) {
                            if ( $contentArr[$i] ) {
                                $itemArr = explode("\t", $contentArr[$i]);
                                $item['spacer_id'] = $itemArr[0];
                                // $ba = explode("|", $itemArr[1]);
                                $item['bacteria_id'] = $itemArr[1];
                                $item['identity'] = $itemArr[2];
                                $item['startPos'] = $itemArr[8];
                                $item['endPos'] = $itemArr[9];
                                $item['evalue'] = $itemArr[10];
                                $item['bitscore'] = $itemArr[11];
                                array_push($proxy, $item);
                            }
                        }
                        $data['data'] = $proxy;
                        $this->ajaxReturn($data);
                    } else {
                        $data['data'] = null;
                        $this->ajaxReturn($data);
                    }
                } else {
                    $data['data'] = null;
                    $this->ajaxReturn($data);
                }
            } else {
                $data['data'] = null;
                $this->ajaxReturn($data);
            }

        } else {
            $this->display("Common/404");
        }
    }

    /**
     * for search 
     * @return [type] [description]
     */
    public function getSelftarget() {
        if ( IS_POST ) {
            $pid = I("post.pid"); // 数据库里的文件路径名对应的id
            $br = M("Bothrefseq");
            $data['data'] = $br->where("refseq_id = '$pid'")->select();
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    public function getClassification() {
        if ( IS_POST ) {
            $pid = I("post.pid"); // 数据库里的文件路径名对应的id
            // $br = M("Subtypes");
            // $data['data'] = $br->where("refseq_id = '$pid'")->select();
            // if ( count($data['data']) ) {
            //     $data['data'] = null;
            // }
            $this->countFilePath($pid);
            $content = file_get_contents($this->filePath . ".cpte") or die("can't get data from $pid.cpte");
            $contentArr = explode('>', trim($content, '>'));
            $data = array();
            for ( $i=0; $i<count($contentArr); $i++ ) {
                $lineArr = explode("\n", str_replace("\r", "", $contentArr[$i]));
                $arr['one'] = $lineArr[0];
                $arr['two'] = $lineArr[1];
                $arr['three'] = $lineArr[2];
                $arr['table'] = array();
                for ( $j=3; $j<count($lineArr); $j++ ) {
                    $ar = explode("\t", $lineArr[$j]);
                    $da['cas_location'] = $ar[0];
                    $da['cas_name'] = $ar[1];
                    $da['cas_profile'] = $ar[2];
                    $da['sub_type'] = $ar[3];
                    $da['e_value'] = $ar[4];
                    array_push($arr['table'], $da);
                }
                array_push($data, $arr);
                // var_dump($data);
            }
            $data = json_encode($data);
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }
    
    public function getInteraction() {
        if ( IS_POST ) {
            $pid = I("post.pid"); // 数据库里的文件路径名对应的id
            $br = M("Interaction");
            $data['data'] = $br->where("bacteria_id = '$pid'")->select();
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    // 获取anticrispr数据
    public function getPredictionAnticrispr() {
        if ( IS_POST ) {
            $pid = I("post.fileId"); // 数据库里的文件路径名对应的id
            $fileTable = M("filename"); // 存储id和文件路径所用的表
            $arr = $fileTable->where("id = ".$pid)->select(); // 根据id寻找出表中对应的文件路径
            $arr2 = explode("/", $arr[0]['name']);
            $num = count($arr2);
            $result = $arr2[$num-1]; // 获取具体的文件名

            $file_title = "/zrom/tmp/tmpanti/".$result.".anti";
            if ( file_exists($file_title) ) {
                $file = fopen($file_title, "r") or die("unable to open the file -- ");
                $first = fgets($file);
                if ( strstr($first, "None") ) {
                    $data['data'] = null;
                    $this->ajaxReturn($data);
                } else {
                    rewind($file);
                    $data = array();
                    $content = fread($file, filesize($file_title));
                    $contentArr = explode("\n", $content);
                    for ( $i=0; $i<count($contentArr); $i++ ) {
                        if ($contentArr[$i]) {
                            $arr3 = explode("\t", $contentArr[$i]);
                            $arr4['bacteria_id'] = $arr3[0];
                            $arr4['anticrispr_msg'] = $arr3[1];
                            $arr4['evalue'] = $arr3[2];
                            $arr4['match_rate'] = $arr3[3];
                            $arr4['coverage'] = $arr3[4];
                            $arr4['protein_sequence'] = $arr3[5];
                            array_push($data, $arr4);
                        }
                    }
                }
                $arr5['data'] = $data;
                // var_dump($arr5);
                $this->ajaxReturn($arr5);
            } else {
                $data['data'] = null;
                $this->ajaxReturn($data);
            }

            $this->ajaxReturn($result);
        } else {
            $this->display("Common/404");
        }
    }

    // 获取Interaction数据
    public function getPredictionInteraction() {
        if ( IS_POST ) {
            $pid = I("post.fileId"); // 数据库里的文件路径名对应的id
            $fileTable = M("filename"); // 存储id和文件路径所用的表
            $arr = $fileTable->where("id = ".$pid)->select(); // 根据id寻找出表中对应的文件路径
            $arr2 = explode("/", $arr[0]['name']);
            $num = count($arr2);
            $result = $arr2[$num-1]; // 获取具体的文件名

            $file_title = "/zrom/tmp/tmpasn/".$result.".res";
            if ( file_exists($file_title) ) {
                $file = fopen($file_title, "r") or die("unable to open the file!!!!");
                $first = fgets($file);
                if ( strstr($first, "None") ) {
                    $data['data'] = null;
                    $this->ajaxReturn($data);
                } else {
                    rewind($file);
                    $data = array();
                    $content = fread($file, filesize($file_title));
                    $contentArr = explode("\n", $content);
                    for ( $i=0; $i<count($contentArr); $i++ ) {
                        if ($contentArr[$i]) {
                            $arr3 = explode("\t", $contentArr[$i]);
                            $arr4['id'] = $arr3[0];
                            $arr4['spacerid'] = $arr3[1];
                            $arr4['identuty'] = $arr3[2];
                            $arr4['coverage'] = $arr3[3];
                            $arr4['hit_len'] = $arr3[4];
                            $arr4['hit_pos'] = $arr3[5];
                            $arr4['spacer_sequence'] = $arr3[6];
                            array_push($data, $arr4);
                        }
                    }
                }
                $arr5['data'] = $data;
                $this->ajaxReturn($arr5);
            } else {
                $data['data'] = null;
                $this->ajaxReturn($data);
            }

            $this->ajaxReturn($result);
        } else {
            $this->display("Common/404");
        }
    }

    // paste sequence
    public function handlePredictionCrispr() {
        if ( IS_POST ) {
            $arr = $_POST;
            $folder = time();
            $uploadPath = '/zrom/upload/'. $folder . '/';
            $isSuccess = mkdir('/zrom/upload/'. $folder);
            if ( $isSuccess ) {
                $cmd = system("chmod 0777 /zrom/upload/".$folder ,$ret);
                file_put_contents($uploadPath.$folder, $arr['ls']);
                $cmd = system("chmod 0777 /zrom/upload/".$folder."/".$folder ,$ret);
                $cmd = system("/zrom/z-tools/bin/call_load ".$uploadPath.$folder, $ret);
                if ( !$ret ) {
                    $this->filePath = $uploadPath.$folder;
                    $pid = $this->getIDByFna($this->filePath);
                    // 将文件名称插入数据
                    // =================================
                    $fileTable = M("Filename");
                    $tableArr['name'] = $this->filePath;
                    $daa = $fileTable->filter("strip_tags")->add($tableArr);
                    if ( $daa ) {
                        // ========================
                        // 获得该文件件名的ID
                        $tableSelectArr = $fileTable->field("id")->where("name = '".$this->filePath."'")->select();
                        $fileId = $tableSelectArr[0]['id'];
                        // ============================
                        $file_name = ".stat";
                        $fp = $this->filePath ."". $file_name;
                        $flag = 1;
                        while ( $flag ) {
                            $text = file_get_contents($fp);
                            if ( strstr($text, "jobs all done!") ) {
                                $flag = 0;
                            }
                        }
//                            $this->assign("fileId", $fileId);
//                            $this->assign("pid", $pid);
//                            $this->display();
                        $pid = str_replace(".", "_", $pid);
                        $this->redirect("Crispr/predictionResult", array("fileId"=>$fileId, "pid"=>$pid));
                    } else {
                        $this->error("There is a error exists!");
                    }
                } else {
                    $this->error("The program running failed!");
                }
            } else {
                $this->error("make file failed!");
            }
        } else {
            $this->error("upload failed!");
        }
    }

//    public function test() {
//        $name = "NC_008532";
//        $this->countFilePath($name);
//        var_dump($this->filePath);
//    }

    // 查询显示结果
    public function handleEntryAccession() {
        // if ( IS_POST ) {
        //     $bacteria_id = I('post.pid');
        //     if ( !str_replace(" ", "", $bacteria_id) ) {
        //         $this->redirect("Common/404");
        //     }
        //     $this->countFilePath($bacteria_id);
        //     $arr = $this->b2->getBacteriaById($bacteria_id);
        //     if ( !count($arr) ) {
        //         $data = array("allLen"=>0);
        //         $this->ajaxReturn($data);
        //     }
        //     // 获取环形数据
        //     $data = $this->getRingData($bacteria_id);
        //     $this->ajaxReturn($data);
        // } else {
        //     $this->display("Common/404");
        // }
        if ( IS_GET ) {
        	$bacteria_id = I('get.pid');
        	if ( !str_replace(" ", "", $bacteria_id) ) {
                $this->redirect("Common/404");
            }
            $this->assign("pid", $bacteria_id);
            $this->display("Crispr/searchResult");
        } else {
        	$this->display("Common/404");
        }
    }



    // 处理sequence序列的
    public function handleSequenceUpload() {
        if ( IS_POST ) {
            $text = I('post.text');
            if ( !str_replace(" ", "", $text) ) {
                $this->redirect("Common/404");
            }
            $folder = time();
            mkdir('/zrom/upload/'. $folder);
            file_put_contents('/zrom/upload/'. $folder .'/'.$folder, $text);


        } else {
            $this->error("upload failed!");
        }
    }


    // *********************************************************
    // two --- crispr
    // *********************************************************

    public function crispr()
    {
        $specieData = $this->b2->getFirstSpecieLevel($this->limitNumber);
        $genusData = $this->b2->getFirstGenusLevel($this->limitNumber);
        $data['specie'] = $specieData;
        $data['genus'] = $genusData;
        $this->assign("data", $data);
        $this->display();
    }



//    public function graph() {
//        $this->display();
//    }

    public function getGraphSelftarget() {
        if ( IS_POST ) {
            $pid = I('post.pid');
            if ( $pid ) {
                $data['data'] = $this->st->where("proto_spacer_accession = '".$pid."'")->select();
                if ( count($data['data']) ) {
                    $this->ajaxReturn($data);
                } else {
                    $data['data'] = null;
                    $this->ajaxReturn($data);
                }

            } else {
                $data['data'] = null;
                $this->ajaxReturn($data);
            }
        } else {
            $data['data'] = null;
            $this->ajaxReturn($data);
        }
    }

    public function getGraphInteraction() {
        if ( IS_POST ) {
            $pid = I('post.pid');
            if ( $pid ) {
                $data['data'] = $this->ir->where("bacteria_id = '".$pid."'")->select();
                if ( count($data['data']) ) {
                    $this->ajaxReturn($data);
                } else {
                    $data['data'] = null;
                    $this->ajaxReturn($data);
                }
            } else {
                $data['data'] = null;
                $this->ajaxReturn($data);
            }
        } else {
            $data['data'] = null;
            $this->ajaxReturn($data);
        }
    }

    public function getPieData() {
        if ( IS_POST ) {
            $sg = D("Speciegenus");
            $arr0 = $sg->field("count(*) as sum")->select();
            $arr1 = $sg->getPieDataForGenus();
            $data['genus'] = $this->transitionToArr($arr1, $arr0[0]['sum']);
            $arr2 = $sg->getPieDataForSpecie();
            $data['specie'] = $this->transitionToArr($arr2, $arr0[0]['sum']);
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    public function transitionToArr($arr,$sum) {
        $array = array();
        $count = 0;
        $other = array("name"=>"others", "value"=>null);
        for ( $i=0; $i<count($arr); $i++ ) {
            array_push($array, $arr[$i]);
            $count += $arr[$i]['value'];
            if ( $count>=0.7*$sum ) {
                break;
            }
        }
        $other['value'] = $sum - $count;
        array_push($array, $other);
        return $array;
    }

    public function getSearchBacteria() {
        if ( IS_POST ) {
            $text = I('post.text');
            $value = I('post.value');
            if ( $value && $text ) {
                if ( $value==1 ) {
                    $where = "name LIKE '%".$text."%'";
                } elseif ( $value==2 ) {
                    $where = "bacteria_id LIKE '%".$text."%'";
                }
                $b2 = D("Bacteria2");
                $searchData = $b2->getSearchBacteria($where);
                $this->ajaxReturn($searchData);
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 大量的bacteria细菌的数据，进行分类获取
    public function handleCrispr()
    {
        if ( IS_POST ) {
            $limit = I('post.limit');
            if ( strlen($limit) ) {
                $b2 = D("Bacteria2");
                $arrList = $b2->getAllCategory(intval($limit), $this->limitNumber);
                $this->ajaxReturn($arrList);
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    public function handleCrispr2() {
        if ( IS_GET ) {
            $data = $this->b2->getThirdLevelBacteria();
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    /**
     * 根据所给的等级获取其子类的数据
     * @return [type] [description]
     */
    public function getSonData() {
        if ( IS_POST ) {
            $level = I('post.level');
            if ( $level ) {
                $sonArr = $this->b2->getSonBacteria2($level);
                $this->ajaxReturn($sonArr);
            } else {
                $data = null;
                $this->ajaxReturn($data);
            }
        } else {
            $this->display("Common/404");
        }
    }

    /**
     * 判断该以其为父节点是否有最底层的bacteria
     * @return boolean [description]
     */
    public function isTheParentOfTheLast(){
        if ( IS_POST ) {
            $level = I('post.level');
            $sonArr = $this->b2->getSonBacteria($level);
            if ( count($sonArr)>0 ) {
                $this->ajaxReturn($sonArr);
            } else {
                $data = null;
                $this->ajaxReturn($data);
            }
        } else {
            $this->display("Common/404");
        }
    }


    public function getTableDataUnderLever() {
        if ( IS_POST ) {
            // $level = I('post.level');
            // $sonArr = $this->b2->getSonBacteria($level);

            $type = I('post.type');
            $name = I('post.name');

            $sonArr = $this->sg->where($type . " = '" . $name . "'")->select();

            // var_dump($sonArr);
            // exit;

            $length = count($sonArr);


            for ( $i=0; $i<count($sonArr); $i++ ) {
            	$flag = false;
                $id = $sonArr[$i]['bacteria_id'];
                $this->countFilePath($id);

                $protein = $this->getCpt2($id);
                if ( !$protein ) {
                    // $sonArr[$i]['protein'] = null;
                    unset($sonArr[$i]);
                    $flag = true;
                } else {
                    $sonArr[$i]['protein'] = $protein;
                    $sonArr[$i]['sum'] = $this->countCasProteinType($protein);
                }

                if ( $flag ) {
                	$sonArr = array_merge($sonArr);
	           		$i --;
	           		continue;
                }
           		

                $class = $this->sts->where("refseq_id = '". $id ."'")->select(); 
                if ( !empty($class) ) {
                    $sonArr[$i]['classification'] = $class[0]['classification'];
                    // $sonArr[$i]['cas_locus'] = $class[0]['cas_locus'];
                } else {
                    $sonArr[$i]['classification'] = null;
                    // $sonArr[$i]['cas_locus'] = null;
                   	// unset($sonArr[$i]);
                }
            }

            $data['data'] = $sonArr;

            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    // 记录cas蛋白所属的类型
    public function countCasProteinType($protein) {
        $res = '# of cas gene = ';
        $proteinArr = explode(',', $protein);
        $num = count($proteinArr);
        $res .= $num . ' ( type ';
        $type = array();
        for ( $i=0; $i<$num; $i++ ) {
            $arr = explode('_', $proteinArr[$i]);
            if ( $arr[1]!='cas1' && $arr[1]!='cas2' && $arr[1]!='cas4' && $arr[1]!='cas6' ) {
                $ar = explode(':', $arr[2]);
                for ( $j=0; $j<count($ar); $j++ ) {
                    $a = explode('-', $ar[$j]);
                    if ( !in_array($a[1], $type) ) {
                        array_push($type, $a[1]);
                    }
                }
                
            }
        }
        // var_dump($type);
        $res .= implode(',', $type) . ' )';
        return $res;
    }

    // public function test() {
    //     $protein = 'cd06127_DEDDh_CAS-I, pfam00078_RT_CAS-I:CAS-III';
    //     var_dump($this->countCasProteinType($protein));
    // }

    // 获取提示数据
    public function getTips()
    {
        if ( IS_POST ) {
            $keyword = I('post.keyword');
            $value = I('post.value');
            if ( $keyword && strlen($keyword)>=4 ) {
                if ( $value == 1 ) {
                    $data = $this->b2->where("name like '%" . $keyword . "%'")->order("name asc")->limit(5)->select();
                } elseif ( $value==2 ) {
                    $data = $this->b2->where("bacteria_id like '%" . $keyword . "%'")->order("bacteria_id asc")->limit(5)->select();
                }
                $this->ajaxReturn($data);
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 获取Specie数据操作 -- 动态加载
    public function getSpecieData() {
        if ( IS_POST ) {
            $limit = I('post.limit');
            if ( strlen($limit) ) {
//                $arrList = $this->b2->getSpecieLevel(intval($limit), $this->limitNumber);
                $arrList = $this->sg->getSpecieLevel(intval($limit), $this->limitNumber);
                $this->ajaxReturn($arrList);
            } else {
                //$this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 获取Genus数据操作 -- 动态加载
    public function getGenusData() {
        if ( IS_POST ) {
            $limit = I('post.limit');
            if ( strlen($limit) ) {
//                $arrList = $this->b2->getGenusLevel(intval($limit), $this->limitNumber);
                $arrList = $this->sg->getGenusLevel(intval($limit), $this->limitNumber);
                $this->ajaxReturn($arrList);
            } else {
                //$this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }


    // 获取某一genus下所有的bacteria
//    public function getSonBacteria(){
//        if ( IS_POST ) {
//            $parent_id = I('post.parent_id');
//            if ( $parent_id ) {
//                $bacterias = $this->b2->getSonBacteria($parent_id);
//                $this->ajaxReturn($bacterias);
//            } else {
//                $this->display("Common/404");
//            }
//        } else {
//            $this->display("Common/404");
//        }
//    }

    public function getSonBacteria() {
        if ( IS_POST ) {
            $type = I('post.type');
            $name = I('post.name');
            if ( $type&&$name ) {
//                $bacterias = $this->b2->getSonBacteria($parent_id);
                $bacterias = $this->sg->getAllLineageForType($type, $name);
                $this->ajaxReturn($bacterias);
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // ====================================================
    // 文件操作
    // ====================================================

    // 获取某个细菌的所有的crispr
    public function getAllLineGraph() {
        if ( IS_POST ) {
            $id = I('post.id'); // bacteria_id
            if ( $id ) {
                $this->countFilePath($id);
                $arr = $this->getCrisprData();
                $children = array();
                if ( count($arr) ) {
                    for ( $j=0; $j<count($arr); $j++ ) {
                        $arr2 = $this->getBacteriaData($id, $arr[$j]['id']);
                        array_push($children, $arr2);
                    }
                }
                $this->ajaxReturn($children);
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }


    // 获取所有的Crispr系统的数据 -- file
    public function getCrisprData() {
//        $file_path = "./admin/files/";
        $file_name = ".csp";
        $file = fopen($this->filePath . $file_name, "r") or die("Unable open file-- getCrisprData!");
        $children = [];

        while( !feof($file) ) {
            $content = fgets($file);
            if ( str_replace("\n", "", $content) ) {
                $conArr = explode("\t", str_replace("\n", "", $content) );
                $arr['id'] = $conArr[0];
                $arr['startPos'] = $conArr[1];
                $arr['length'] = $conArr[2];
                $arr['pmc'] = $conArr[3];
                array_push($children, $arr);
            }
        }
        return $children;
    }


//    public function showGraph() {
//        if ( IS_GET ) {
//            $bacteria_id = $_GET['pid'];
//            $this->redirect("Crispr/graph", array("bacteria_id"=>$bacteria_id));
//        } else {
//            $this->display("Common/404");
//        }
//    }

    // 图形显示界面
    public function graph(){
        $this->display();
    }

    // Ajax获取环形图像的数据 -- file
    public function handleGraph() {
        if ( IS_POST ) {
            $pid = I('post.pid');
            if ( !str_replace(" ", "", $pid) ) {
                $this->redirect("Common/404");
            }
            $this->countFilePath($pid);
            // 获取环形数据
            $data = $this->getRingData($pid);
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    public function handlePredictonGraph() {
        if ( IS_POST ) {
            $pid = I('post.pid'); // pid 代表path

            if ( !str_replace(" ", "", $pid) ) {
                $this->redirect("Common/404");
            }
            // ==============
            $fileTable = M("filename");
            $arr = $fileTable->where("id = ".$pid)->select();
            $this->filePath = $arr[0]['name'];
            // 获取环形数据
            $data = $this->getRingData2();
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    /**
     * 获取搜索操作的图数据
     * @return [type] [description]
     */
    public function handleSearchGraph() {
        if ( IS_POST ) {
            $pid = I('post.pid'); // pid 代表path
            if ( !str_replace(" ", "", $pid) ) {
                $this->redirect("Common/404");
            }
            $this->countFilePath($pid);
            // echo $this->filePath;
            $data = $this->getRingData($pid);
            $this->ajaxReturn($data);
        } else {
            $this->display("Common/404");
        }
    }

    // 获取环形数据
    public function getRingData($pid) {
        
        // 获取数据库中的 Prophage region 和 Genomic island 数据
        $linkData = $this->b2->where("bacteria_id = '" . $pid . "'")->select();       




        $file_name = ".csp";
        $file = fopen($this->filePath . $file_name, "r");
        if ( !$file ) {
            return null;
        }
        $data = [];
        $children = [];

        while( !feof($file) ) {
            $content = fgets($file);
            if ( str_replace("\n", "", $content) ) {
                $conArr = explode("\t", str_replace("\n", "", $content) );
                $arr['id'] = $conArr[0];
                $arr['startPos'] = $conArr[1];
                $arr['length'] = $conArr[2];
                $arr['pmc'] = $conArr[3];
                array_push($children, $arr);
            }
        }

        $data['allLen'] = $this->countDnaLength($this->filePath . ".fna");
        $nameArr = $this->b2->field("name")->where("bacteria_id = '". $pid . "'")->select();
        $data['title'] = $nameArr[0]['name'];
        $data['children'] = $children;
        $ring1 = M("Ring1");
        $ring2 = M("Ring2");
        $inData = $ring1->field("start_coord, end_coord")->where("accession = '" . $pid . "'")->select();
        $outData = $ring2->field("start, end")->where("accession_number like '" . $pid . "%'")->select();
        $data['in'] = $inData;
        $data['out'] = $outData;
        $data['link'] = $linkData[0];
        return $data;
    }

    // 获取环形数据
    public function getRingData2() {


        // 获取数据库中的 Prophage region 和 Genomic island 数据
        $linkData = $this->b2->where("bacteria_id = '" . $pid . "'")->select();   


        $file_name = ".csp";
        $fp = $this->filePath ."". $file_name;
        $file = fopen($fp, "r") or die("Unable open file!-- getRingData2");
        $data = [];
        $children = [];

        while( !feof($file) ) {
            $content = fgets($file);
            if ( str_replace("\n", "", $content) ) {
                $conArr = explode("\t", str_replace("\n", "", $content) );
                $arr['id'] = $conArr[0];
                $arr['startPos'] = $conArr[1];
                $arr['length'] = $conArr[2];
                $arr['pmc'] = $conArr[3];
                array_push($children, $arr);
            }
        }
        if ( $this->filePath=="/zrom/jobs/bacteria/100/NC_017545/NC_017545" ) {
            $pid = $this->getIDByFna($this->filePath.".fna");
            $data['allLen'] = $this->countDnaLength($this->filePath.".fna");
        } else {
            $pid = $this->getIDByFna($this->filePath);
            $data['allLen'] = $this->countDnaLength($this->filePath);
        }

        $data['children'] = $children;
        // $ring1 = M("Ring1");
        // $ring2 = M("Ring2");
        // $inData = $ring1->field("start_coord, end_coord")->where("accession = '" . $pid . "'")->select();
        // $outData = $ring2->field("start, end")->where("accession_number like '" . $pid . "%'")->select();
        // $data['in'] = $inData;
        // $data['out'] = $outData;
        $data['in'] = [];
        $data['out'] = [];
        $data['bacteria_id'] = $pid;
        $data['filepath'] = $this->filePath;
        $data['link'] = $linkData;
        return $data;
    }

    // 获取线性图所需要的数据
    public function getLineData() {
        if ( IS_POST ) {
            $id = I('post.id');
            $pid = I('post.pid');
            if ( str_replace(" ", "", $id) &&  str_replace(" ", "", $pid) ) {
                $this->countFilePath($pid);
                $this->folder = $pid;
                $data = $this->getBacteriaData($pid, $id);
                $this->ajaxReturn($data);
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 获取线性图的数据---prediction
    public function getPredictionLineData() {
        if ( IS_POST ) {
            $id = I('post.id');
            $fileId = I('post.fileId');
            $pid = I('post.pid');
            if ( str_replace(" ", "", $id) &&  str_replace(" ", "", $fileId) ) {
//                $this->countFilePath($pid);
                // ==============
                $fileTable = M("filename");
                $arr = $fileTable->where("id = ".$fileId)->select();
                $this->filePath = $arr[0]['name'];
//                $this->folder = $pid;
                $data = $this->getBacteriaData($pid, $id);
                $this->ajaxReturn($data);
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    /**
     * 获取查询的图的线性数据
     * @return [type] [description]
     */
    // public function getSearchLineData() {
    //      if ( IS_POST ) {
    //         $id = I('post.id');
    //         $pid = I('post.pid');
    //         if ( str_replace(" ", "", $id) &&  str_replace(" ", "", $fileId) ) {
    //             // ==============
    //             $fileTable = M("filename");
    //             $arr = $fileTable->where("id = ".$fileId)->select();
    //             $this->filePath = $arr[0]['name'];
    //             $data = $this->getBacteriaData($pid, $id);
    //             $this->ajaxReturn($data);
    //         } else {
    //             $this->display("Common/404");
    //         }
    //     } else {
    //         $this->display("Common/404");
    //     }
    // }

    // 计算文件的路径
    public function countFilePath($pid) {
        $num = 0;
        for ( $i=0; $i<strlen($pid); $i++ ) {
            if ( $pid[$i]!=" " ) {
                $num += ord($pid[$i]);
            }
        }
        $num %= 150;
//        $this->countFilePath($pid);
        $this->filePath = "/zrom/jobs/bacteria/" . $num . "/" . $pid . "/" . $pid;
    }

    // 计算文件的路径 -- 返回计算得出的数值
    public function countFilePath2($pid) {
        $num = 0;
        for ( $i=0; $i<strlen($pid); $i++ ) {
            if ( $pid[$i]!=" " ) {
                $num += ord($pid[$i]);
            }
        }
        $num %= 150;
        return "/zrom/jobs/bacteria/".$num. "/" . $pid . "/" . $pid;
    }

    // 获取cas protein info
    public function getProteinInfo(){
        if ( IS_GET ) {
            $pid = I('get.pid');
            $id = I('get.id');
            if ( str_replace(" ", "", $pid) ) {
                $this->countFilePath($pid);
                $proteinsInfo = $this->getCpt($id);
                $this->assign("arrList", $proteinsInfo);
                $this->display();
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 获取cas protein info -- prediction
    public function getPredictionProteinInfo(){
        if ( IS_GET ) {
            $pid = I('get.pid');
            $id = I('get.id');
            if ( str_replace(" ", "", $pid) ) {
                // ==============
                $fileTable = M("filename");
                $arr = $fileTable->where("id = ".$pid)->select();
                $this->filePath = $arr[0]['name'];
                $proteinsInfo = $this->getCpt($id);
                $this->assign("arrList", $proteinsInfo);
                $this->display("Crispr/getProteinInfo");
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    /**
     * 获取cas protein info -- search
     * @return [type] [description]
     */
    public function getSearchProteinInfo() {
        if ( IS_GET ) {
            $pid = I('get.pid');
            $id = I('get.id');
            if ( str_replace(" ", "", $pid) ) {
                $this->countFilePath($pid);
                $proteinsInfo = $this->getCpt($id);
                $this->assign("arrList", $proteinsInfo);
                $this->display("Crispr/getProteinInfo");
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 获取crispr locus info
    public function getRepeatSpacerInfo() {
        if ( IS_GET ) {
            $pid = I('get.pid');
            $id = I('get.id');
            if ( str_replace(" ", "", $pid) ) {
                $this->countFilePath($pid);
                $content = file_get_contents($this->filePath . ".tmp");
                $start = strpos($content, "Array");
                $cont = substr($content, $start);
                $this->assign("content", $cont);
                $this->display();
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 获取crispr locus info -- prediction
    public function getPredictionRepeatSpacerInfo() {
        if ( IS_GET ) {
            $pid = I('get.pid');
            $id = I('get.id');
            if ( str_replace(" ", "", $pid) ) {
                // ==============
                $fileTable = M("filename");
                $arr = $fileTable->where("id = ".$pid)->select();
                $this->filePath = $arr[0]['name'];
                $content = file_get_contents($this->filePath . ".tmp");
                $start = strpos($content, "Array");
                $cont = substr($content, $start);
                $this->assign("content", $cont);
                $this->display("Crispr/getRepeatSpacerInfo");
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 获取显示的所有蛋白质信息
    public function getProtein() {
        if ( IS_GET ) {
            $pid = I('get.pid');
            $id = I('get.id');
            if ( str_replace(" ", "", $pid) ) {
                $this->countFilePath($pid);
                $proteins = $this->getProteinData2($id);
                $this->assign("proteins", $proteins);
                $this->display();
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 获取显示的所有蛋白质信息 -- prediction
    public function getPredictionProtein() {
        if ( IS_GET ) {
            $pid = I('get.pid');
            $id = I('get.id');
            if ( str_replace(" ", "", $pid) ) {
                // ==============
                $fileTable = M("filename");
                $arr = $fileTable->where("id = ".$pid)->select();
                $this->filePath = $arr[0]['name'];
                $proteins = $this->getProteinData2($id);
                $this->assign("proteins", $proteins);
                $this->display("Crispr/getProtein");
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }


    // 获取显示的所有Spacers信息
    public function getSpacer() {
        if ( IS_GET ) {
            $pid = I('get.pid'); // folder
//            $savename = I('get.name');
            $id = I('get.id');
            if ( str_replace(" ", "", $pid) ) {
                $this->countFilePath($pid);
//                $this->filePath = "/zrom/upload/".$pid."/".$savename;
                $spacers = $this->getSpacerData($pid, $id);
                uasort($spacers, $this->sort_by_pos);
                $this->assign("spacers", $spacers);
                $this->display();
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 获取显示的所有Spacers信息 --- prediction
    public function getPredictionSpacer() {
        if ( IS_GET ) {
            $pid = I('get.pid'); // fileID
            $id = I('get.id');
            if ( str_replace(" ", "", $pid) ) {
                // ==============
                $fileTable = M("filename");
                $arr = $fileTable->where("id = ".$pid)->select();
                $this->filePath = $arr[0]['name'];
                $spacers = $this->getSpacerData($pid, $id);
                uasort($spacers, $this->sort_by_pos);
                $this->assign("spacers", $spacers);
                $this->display("Crispr/getSpacer");
            } else {
                $this->display("Common/404");
            }
        } else {
            $this->display("Common/404");
        }
    }

    // 自定义排序算法
    public function sort_by_pos($x,$y){
        return $x['startPos']+$x['logicalStart'] - $y['startPos'] - $y['logicalStart'];
    }

    // 获取显示的所有细菌上所有有用的信息
    public function getBacteriaData($pid, $id) {
        $data = [];
        $selfArr = [];

        $protein = $this->getProteinData($id);

        $spacers = $this->getSpacerData($pid, $id);

//        $commons = $this->getCommons($id);

        $data['id'] = $id;
        $data['protein'] = $protein;
        $data['spacers'] = $spacers;

        // 判断repeat+spacer是否存在
        $data['repeat_spacer'] = $this->isRepeatSpacerExists();

//        $selfArr['spacers'] = $spacers;
//        $selfArr['commons'] = $commons;

        $data2['one'] = $data;
//        $data2['two'] = $selfArr;
        $isExists = $this->ir->checkExists($pid, $spacers);
        $data2['exists'] = $isExists;
        return $data2;
    }

    function isRepeatSpacerExists($pid) {
        $this->countFilePath($pid);
        $file = $this->filePath . ".tmp";
        if ( file_exists($file) ) {
            return true;
        } else {
            return false;
        }
    }

    // 获取蛋白质的数据
    public function getProteinData($id) {
//        $file_name1 = "./admin/files/NZ_KK328771.cpt";
        $file_name1 = ".cpt";
        $file_name2 = ".ffn";
        $file_name4 = ".faa";

        $protein = [];

        $file1 = fopen($this->filePath ."". $file_name1, "r") or die("Unable open file555!");
        while( !feof($file1) ) {
            $content = fgets($file1);
            if ( $row = str_replace("\n", "", $content) ) {
                $columns = explode("\t", $row); // 列数组
                $cpt = explode("_", $columns[0]); //细菌名 + 所属id
                $len = count($cpt);
                $startPos = $cpt[$len-4];
                $endPos = $cpt[$len-3];
                $pmc = $cpt[$len-2];
                $fid = array_pop($cpt);
                if ( $fid==$id ) {
                    $cptStr = implode("_", $cpt);
                    $bacteria['bacteria_name'] = $cptStr;
                    $bacteria['startPos'] = $startPos;
                    $bacteria['endPos'] = $endPos;
                    $bacteria['pmc'] = $pmc;
                    $bacteria['protein_name'] = $columns[1];
                    $bacteria['evalue'] = $columns[2];
                    $bacteria['score'] = $columns[3];
                    $bacteria['bias'] = $columns[4];
                    $bacteria['bias'] = $columns[4];
//                    $bacteria['hit_type'] = $columns[3];
//                    $bacteria['accessionID'] = $columns[4];
//                    $bacteria['logicalStart'] = $columns[5];
//                    $bacteria['logicalEnd'] = $columns[6];
//                    $bacteria['evalue'] = $columns[7];
//                    $bacteria['hit-score'] = $columns[8];
//                    $bacteria['protein_name'] = $columns[10];
//                    $bacteria['description'] = $columns[12];
//                    $bacteria['dna'] = null;
//                    $bacteria['protein_sequence'] = null;
//                    $bacteria['title'] = ">" . $cpt[0] . "\t" . $cpt[1] . "\t" . $cpt[2] . "\t" . $columns[1];
//                    $bacteria['protein_sequence'] = null;
//                    $bacteria['dna'] = null;
                    array_push($protein, $bacteria);
                }
            }
        }
        fclose($file1);

//        $file2 = fopen($this->filePath . $file_name2, "r") or die("Unable open file444!");
//        $i = 0;
//        while( $i<count($protein) ) {
//            while ( !feof($file2) ) {
//                $row = str_replace("\n", "", fgets($file2));
//                if ( $row ) {
//                    $name = str_replace(" ", "", str_replace(">", "", $row));
//                    if ( $name==$protein[$i]['bacteria_name'] ) {
//                        $protein[$i]['dna'] = str_replace("\n", "", fgets($file2));
//                        rewind($file2);
//                        $i ++;
//                        break;
//                    }
//                } else {
//                    fgets($file2);
//                }
//            }
//        }
//        fclose($file2);

        $file4 = fopen($this->filePath ."". $file_name4, "r") or die("Unable open file333!");
        $i = 0;
        while( $i<count($protein) ) {
            while ( !feof($file4) ) {
                $row = str_replace("\n", "", fgets($file4));
                if ( $row ) {
                    $name = str_replace(" ", "", str_replace(">", "", $row));
                    if ( $name==$protein[$i]['bacteria_name'] ) {
                        $protein[$i]['protein_sequence'] = str_replace("\n", "", fgets($file4));
                        rewind($file4);
                        $i ++;
                        break;
                    }
                } else {
                    fgets($file4);
                }
            }
        }
        fclose($file4);

        return $protein;
    }

    public function getProteinData2($id) {
//        $file_name1 = "./admin/files/NZ_KK328771.cpt";
        $file_name1 = ".cpt";
//        $file_name4 = "./admin/files/NZ_KK328771.faa";
        $file_name4 = ".faa";

        $protein = [];

        $file1 = fopen($this->filePath . $file_name1, "r") or die("Unable open file5555555555! -- getProteinData2");
        while( !feof($file1) ) {
            $content = fgets($file1);
            if ( $row = str_replace("\n", "", $content) ) {
                $columns = explode("\t", $row); // 列数组
                $cpt = explode("_", $columns[0]); //细菌名 + 所属id
                $fid = array_pop($cpt);
                if ( $fid==$id ) {
                    $cptStr = implode("_", $cpt);
                    $bacteria['bacteria_name'] = $cptStr;
                    $bacteria['title'] = ">" . $cpt[0] . "\t" . $cpt[1] . "\t" . $cpt[2] . "\t" . $columns[1];
                    $bacteria['protein_sequence'] = '';
                    $bacteria['dna'] = '';
                    array_push($protein, $bacteria);
                }
            }
        }
        fclose($file1);

        $file4 = fopen($this->filePath . $file_name4, "r") or die("Unable open file33333333333! -- getProteinData2");
        $i = 0;
        while( $i<count($protein) ) {
            while ( !feof($file4) ) {
                $row = str_replace("\n", "", fgets($file4));
                if ( $row ) {
                    $name = str_replace(" ", "", str_replace(">", "", $row));
                    if ( $name==$protein[$i]['bacteria_name'] ) {
                        $protein[$i]['protein_sequence'] = str_replace("\n", "", fgets($file4));
                        rewind($file4);
                        $i ++;
                        break;
                    } else {
                        fgets($file4);
                    }
                } else {
                    fgets($file4);
                }
            }
//            $i ++;
        }
        fclose($file4);

        return $protein;
    }

    // 获取cpt文件 -- file
    public function getCpt($id) {
        $file_name1 = ".cpt";
        $protein = [];
        $file1 = fopen($this->filePath ."". $file_name1, "r") or die("Unable open file!-- getCpt");
        while( !feof($file1) ) {
            $content = fgets($file1);
            if ( $row = str_replace("\n", "", $content) ) {
                $columns = explode("\t", $row); // 列数组
                $cpt = explode("_", $columns[0]); //细菌名 + 所属id
                $len = count($cpt);
                $fid = array_pop($cpt);
                if ( $fid==$id ) {
                    array_push($protein, $columns);
                }
            }
        }
        fclose($file1);
        return $protein;
    }

    /**
     * 获取cpt文件，在/zrom/jobs/bacteria文件下
     * @return [type] [description]
     */
    public function getCpt2($id) {
        $file_name1 = ".cpt";
        $protein = "";
        if ( !file_exists($this->filePath . "" . $file_name1) ) {
            return null;
        }
        $file1 = fopen($this->filePath ."". $file_name1, "r") or die("Unable open file!-- getCpt");
        while( !feof($file1) ) {
            $content = fgets($file1);
            if ( $row = str_replace("\n", "", $content) ) {
                $columns = explode("\t", $row); // 列数组
                $cpt = explode("|", $columns[0]); //细菌名 + 所属id
                $len = count($cpt);
                $cpt_id = explode(".", $cpt[1]);
                $fid = $cpt_id[0];
                if ( $fid==$id ) {           
                    $protein .= $columns[5] . ', ';
                }
            }
        }
        fclose($file1);
        $protein = substr($protein, 0, count($protein)-3);
        return $protein;
    }

    // 获取spacer的数据
    public function getSpacerData($bacteria_id, $id) {
        $file_name3 = ".spc";
//        var_dump($this->filePath ."". $file_name3);
        $file3 = fopen($this->filePath ."". $file_name3, "r") or die("Unable open file222!-- getSpacerData");
        $spacers = [];
        $ir = D("Interaction");
        while ( !feof($file3) ) {
            $content = fgets($file3);
            if ( $row = str_replace("\n", "", $content) ) {
                $row = str_replace(">", "", $row);
                $rowArr = explode("|", $row);
                $fid = explode(".", $rowArr[0])[0];
                if ( $fid==$id ) {
                    $spacer['id'] = $rowArr[0];
                    $spacer['startPos'] = $rowArr[1];
                    $spacer['len'] = $rowArr[2];
                    $spacer['dna'] = str_replace("\n", "", fgets($file3));
                    array_push($spacers, $spacer);
                }
            } else {
                fgets($file3);
            }
        }
        fclose($file3);
        return $spacers;
    }

    // 获取self-targeting的数据
//    public function getCommons($id) {
//        $file_name5 = ".fasn";
//        $commons = [];
//
//        $file5 = fopen($this->filePath . $file_name5, "r") or die("Unable open file111!");
//        while( !feof($file5) ) {
//            $row = str_replace("\n", "", fgets($file5));
//            if ( $row ){
//                $rowArr = explode("\t", $row);
//                $parent = explode("|", $rowArr[1]);
//                $name = explode(".", $parent[0]);
//                if ( $name[0]==$id ) {
//                    $aaa['starPos'] = $rowArr[9];
//                    $aaa['endPos'] = $rowArr[10];
//                    $aaa['evalue'] = $rowArr[11];
//                    $aaa['parent_id'] = $parent[0];
//                    $aaa['pmc'] = $rowArr[0];
//                    array_push($commons, $aaa);
//                }
//
//            }
//        }
//        fclose($file5);
//        return $commons;
//    }

    // 获取细菌基因的长度
    public function countDnaLength($filename) {
        $file = fopen($filename, "r") or die("Unable open file -- countDnaLength");
        if ( $file ) {
            $content = fread($file, filesize($filename));
            $arr = explode("\n", $content);
            $data = implode("\n", array_slice($arr, 1));
            $cnt = trim($data, " \n");
            $len = strlen($cnt);
            fclose($file);
            return $len;
        } else {
            return null;
        }
    }

    // 根据fna文件获取细菌ID
    public function getIDByFna($filename) {
        $file = fopen($filename, "r") or die("Unable open file -- getIDByFna");
        if ( $file ) {
            $content = fread($file, filesize($filename));
            $arr = explode("\n", $content);
            $pidArr = explode("|", $arr[0]);
            $pid = str_replace(" ", "", $pidArr[1]);
            return $pid;
        } else {
            return null;
        }
    }

    public function getNameById() {
        if ( IS_POST ) {
            $pid = I('pid');
            $b2 = D("Bacteria2");
            $arr = $b2->where("bacteria_id = '".$pid."'")->select();
            $this->ajaxReturn($arr);
        } else {
            $this->display("Common/404");
        }
    }

    public function getPredictionProcess() {
        
    }

}