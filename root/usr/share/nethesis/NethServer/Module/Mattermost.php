<?php
namespace NethServer\Module;

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

class Mattermost extends \Nethgui\Controller\CompositeController implements \Nethgui\Component\DependencyConsumer
{

    protected function initializeAttributes(\Nethgui\Module\ModuleAttributesInterface $attributes)
    {
        return new \NethServer\Tool\CustomModuleAttributesProvider($attributes, array(
            'category' => 'Configuration')
        );
    }

    public function initialize()
    {
        parent::initialize();
        $this->addChild(new Mattermost\Main());
        $this->addChild(new Mattermost\ImportUsers());
    }

    public function setUserNotifications(\Nethgui\Model\UserNotifications $n)
    {
        $this->notifications = $n;
        return $this;
    }

    public function setSystemTasks(\Nethgui\Model\SystemTasks $t)
    {
        $this->systemTasks = $t;
        return $this;
    }

    public function getDependencySetters()
    {
        return array(
            'UserNotifications' => array($this, 'setUserNotifications'),
            'SystemTasks' => array($this, 'setSystemTasks'),
        );
    }

    public function prepareView(\Nethgui\View\ViewInterface $view)
    {
        parent::prepareView($view);
        if($this->getRequest()->hasParameter('installSuccess')) {
            $view->getCommandList()->show();
        } elseif($this->getRequest()->hasParameter('installFailure')) {
            $taskStatus = $this->systemTasks->getTaskStatus($this->getRequest()->getParameter('taskId'));
            $data = \Nethgui\Module\Tracker::findFailures($taskStatus);
            $this->notifications->trackerError($data);
            $view->getCommandList('Main')->show();
        }
    }

}
