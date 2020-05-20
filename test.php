<?php
// OAuthライブラリの読み込み
require "twitteroauth/autoload.php";
use Abraham\TwitterOAuth\TwitterOAuth;
//認証情報
$consumerKey = "xp8MDAfRkMQ1vgNYOARhUFmaS";
$consumerSecret = "yqmHpPOOXtEjsHdmRpmFXWKpmNJxQsRZwSZJ7pcYOHnjdy1X2K";
$accessToken = "1261849493726617600-VHnpofU0e0QmAbmBgO1bgxVKHvVp41";
$accessTokenSecret = "tQM5SbEHyE6NM9AoBHifLlE5ZL3WqcgVNZyqQrwOpKkKF";
//自分のスクリーンネーム
$screen_name = "starwing_timesignal";

//接続
$connection = new TwitterOAuth($consumerKey, $consumerSecret, $accessToken, $accessTokenSecret);

/* //リプライを10件取得
$res = $connection->get("statuses/mentions_timeline", array("count" => "10"));

//リプライを取り出し
for ($i=0; $i < count($res); $i++) {
  //リプライにおやすみが含まれていたら
  if(strpos($res[$i]->text,'') !== false){
    //自分のツイートじゃなかったら
    if ($res[$i]->user->screen_name !== $screen_name) {
      //おやありとリプ
      $rp = $connection-  >post("statuses/update", array("status" => "@".$res[$i]->user->screen_name."
    おやあり！","in_reply_to_status_id" => $res[$i]->id));
      //ファボる
      $fav = $connection->post("favorites/create", array("id" => $res[$i]->id));
    }
  } 

} */

// oAuth認証を利用し、twitterに投稿する
$TWITTER_STATUS_UPDATE_URL = "http://api.twitter.com/1.1/statuses/update.json";
$method  = 'POST';
$message = 'テスト';

$response = $oAuth->post('statuses/update', array('status' => $message));

// 結果出力
var_dump($response);

?>
