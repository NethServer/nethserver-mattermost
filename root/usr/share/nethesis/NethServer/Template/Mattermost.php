<?php

echo $view->header()->setAttribute('template', $T('Mattermost_Title'));

$url = $view->getModuleUrl('/Pki');
$info = "<div class='mattermost-info'><p><span class='fa fa-info-circle'></span>".$T('info_label', array($T('LetsEncryptDomains_label'),$T('Pki_Title')))."</p></div>";

echo $view->panel()
    ->insert($view->fieldsetSwitch('status', 'enabled', $view::FIELDSETSWITCH_CHECKBOX | $view::FIELDSETSWITCH_EXPANDABLE)->setAttribute('uncheckedValue', 'disabled')
        ->insert($view->panel()->insert($view->literal($info)))
        ->insert($view->textInput('VirtualHost')->setAttribute('placeholder',$view['DefaultUrl']))
    );

echo $view->buttonList($view::BUTTON_SUBMIT | $view::BUTTON_HELP);

$view->includeCss("
.mattermost-info { padding: 10px; margin: 10px; border: 1px solid #c2c2c2; width: 50%; background-color: #eee }
.mattermost-info .fa { padding-right: 5px }
");

