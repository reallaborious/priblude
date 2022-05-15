<form action="" method="post">
    <label>test <input type="text" name="sender" value=""></label><br>
    <input type="submit" value="submit">
</form>
<?php
if (isset($_POST['sender'])) {
    $subject = 'test mail';
    $mess = 'test mail from script';
    $to = $_POST['sender'];
    if (mail($to, $subject, $mess)) {
        echo 'Message sent';
    } else {
        echo 'Failed';
    }
}
?>

