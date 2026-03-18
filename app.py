<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mobile = $_POST['mobile'];
    $message = $_POST['message'];
    
    // Ining Token makuha mo sa SMS Mobile API Dashboard
    $token = "713191dc709240fcab00fd4d698b39cee95d0bedc0067c08";

    $url = "https://smsmobileapi.com/api/v1/sms/send";
    $data = array(
        "mobile" => $mobile,
        "message" => $message,
        "token" => $token
    );

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    
    $result = curl_exec($ch);
    curl_close($ch);
    
    echo "Result: " . $result;
}
?>

<form method="post">
    <input type="text" name="mobile" placeholder="+639..." required><br>
    <textarea name="message" required></textarea><br>
    <button type="submit">Send SMS</button>
</form>
