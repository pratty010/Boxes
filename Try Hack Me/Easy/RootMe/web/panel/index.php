<?php
session_start();
// if (!isset($_SESSION['admin'])){
//     header('Location: ../admin');
// }

$uploadOk = 2;

if (isset($_POST["submit"])){
    $target_dir = "../uploads/";
    $target_file = $target_dir . basename($_FILES["fileUpload"]["name"]);
    $file_filetype = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

    if ($file_filetype == "php"){
        $result = "PHP não é permitido!";
        $uploadOk = 0;
    } else {
        if (file_exists($target_file)){
            $result = "O arquivo já existe.";
            $uploadOk = 0;
        }
        if (move_uploaded_file($_FILES["fileUpload"]["tmp_name"], $target_file)) {
            $result = "O arquivo foi upado com sucesso!";
            $uploadOk = 1;
            // if ($file_filetype == "php1" || $file_filetype == "php2" || $file_filetype == "php3" || $file_filetype == "php4" || $file_filetype == "php5" || $file_filetype == "php6" || $file_filetype == "php7" || $file_filetype == "php8" || $file_filetype == "php9"){
            //     $result = "hackIT{uplo4d_f1l3_byp4ss}";;
            // }
        } else {
            $result = "Erro enviando o arquivo!";
            $uploadOk = 0;
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../css/panel.css">
    <script src=../"js/maquina_de_escrever.js"></script>
    <title>HackIT - Home</title>
</head>
<body>
    <div class="first">
        <div class="main-div">
            <form action="" method="POST" enctype="multipart/form-data">
                <p>Select a file to upload:</p>
                <input type="file" name="fileUpload" class="fileUpload">
                <input type="submit" value="Upload" name="submit">
                
                <?php
                  if ($uploadOk == 1){
                    echo "<p class='success'>{$result}</p>";
                    echo "<a href='{$target_file}'>Veja!</a>";
                  } elseif ($uploadOk == 0){
                    echo "<p class='erro'>{$result}</p>";
                  }
                ?>
            </form>
        </div>
    </div>
</body>
</html>
