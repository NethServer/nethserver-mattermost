<?php

echo $view->header()->setAttribute('template', $T('ImportUsers_header'));

echo $view->textLabel('Message');

echo $view->fieldset('')->setAttribute('template', $T('HelperOutput_label'))
    ->insert($view->textArea('HelperOutput', $view::STATE_READONLY | $view::LABEL_NONE)->setAttribute('dimensions', '25x80'));

echo $view->buttonList($view::BUTTON_CANCEL | $view::BUTTON_HELP)->insert($view->button('ImportUsersSubmit', $view::BUTTON_SUBMIT));

$actionId = $view->getUniqueId();
$buttonTarget = $view->getClientEventTarget('ImportUsersSubmit');

$view->includeJavascript("
jQuery(function($) {
    $('#${actionId} form').on('submit', function () {
        $('.${buttonTarget}').button('disable');
    });
});
");