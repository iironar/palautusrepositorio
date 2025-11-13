*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  saatana
    Set Password  kalle123
    Set Password confirmation  kalle123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  sa
    Set Password  kalle123
    Set Password confirmation  kalle123
    Click Button  Register
    Register Should Fail With Message  Username is too short

Register With Valid Username And Too Short Password
    Set Username  saatana
    Set Password  ka
    Set Password confirmation  ka
    Click Button  Register
    Register Should Fail With Message  Password is too short

Register With Valid Username And Invalid Password
# salasana ei sisällä halutunlaisia merkkejä
    Set Username  saatana
    Set Password  kakakakaka
    Set Password confirmation  kakakakaka
    Click Button  Register
    Register Should Fail With Message  Password cant consist of only letters


Register With Nonmatching Password And Password Confirmation
    Set Username  saatana
    Set Password  kakakakaka1212
    Set Password confirmation  kakakakak1212
    Click Button  Register
    Register Should Fail With Message  Passwords dont match

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kakakakaka22
    Set Password confirmation  kakakakaka22
    Click Button  Register
    Register Should Fail With Message  Username already exists

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page

Register Should Succeed
    Title Should Be  Welcome to Ohtu Application!

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Register Page Should Be Open
    Title Should Be  Register

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}