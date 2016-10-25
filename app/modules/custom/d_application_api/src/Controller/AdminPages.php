<?php

namespace Drupal\d_application_api\Controller;

use Drupal\Core\Controller\ControllerBase;

/**
 * Class AdminPages
 * @package Drupal\d_application_api\Controller
 */
class AdminPages extends ControllerBase {
  public function applicationMainPage() {

    if (\Drupal::moduleHandler()->moduleExists('masquarade')) {
      $masquarade_block = \Drupal::formBuilder()
                                 ->getForm('Drupal\masquerade\Form\MasqueradeForm');
    }
    else {
      $masquarade_block = NULL;
    }

    $output = '';
    $output .= '<p>' . $this->t('Main page for application pages.') . '</p>';
    $output .= '<br>';
    $output .= 'Switch user';


    return array(
      '#markup' => $output,
      $masquarade_block,
    );

  }

  public function applicationAdministrationViews() {
    $output = '';
    $output .= '<p>' . $this->t('Plceholder for views.') . '</p>';

    return array(
      '#markup' => $output,
    );
  }

}
