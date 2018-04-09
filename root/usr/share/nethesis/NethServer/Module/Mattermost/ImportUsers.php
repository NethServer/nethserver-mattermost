<?php

namespace NethServer\Module\Mattermost;

/*
 * Copyright (C) 2018 Nethesis S.r.l.
 * 
 * This script is part of NethServer.
 * 
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see <http://www.gnu.org/licenses/>.
 */

use Nethgui\System\PlatformInterface as Validate;

class ImportUsers extends \Nethgui\Controller\AbstractController implements \Nethgui\Component\DependencyConsumer
{
    protected $helperProcess = NULL;
    
    public function initialize()
    {
        
    }
    
    public function process()
    {
        parent::process();
        if($this->getRequest()->isMutation()) {
            $this->helperProcess = $this->getPlatform()->exec('/usr/bin/sudo /usr/sbin/mattermost-bulk-user-create 2>&1');
        }
    }
    
    public function prepareView(\Nethgui\View\ViewInterface $view)
    {
        parent::prepareView($view);
        if(isset($this->helperProcess)) {
            $view['HelperOutput'] = $this->helperProcess->getOutput();
            if($this->helperProcess->getExitCode() == 0) {
                $this->notifications->message($view->translate('ImportUsersCommand_success'));
            } else {
                $this->notifications->error($view->translate('ImportUsersCommand_failure'));
            }
        }
        if($this->getRequest()->isValidated()) {
            $view->getCommandList()->show();
        }
    }


    public function setUserNotifications(\Nethgui\Model\UserNotifications $n)
    {
        $this->notifications = $n;
        return $this;
    }

    public function getDependencySetters()
    {
        return array(
            'UserNotifications' => array($this, 'setUserNotifications'),
        );
    }
}