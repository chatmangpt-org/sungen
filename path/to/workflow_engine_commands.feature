Feature: Workflow Engine CLI Commands

  Scenario: Interact with the workflow engine
    Given I have the YAML file "morning_routine.yaml"
    When I convert the YAML to XML using the command "python yaml_to_xml_converter.py morning_routine.yaml morning_routine.xml"
    Then the XML file "morning_routine.xml" should be created

    When I start the workflow engine using the command "docker-compose up"
    Then the workflow engine should be running

    When I deploy the BPMN file using the command "curl -X POST -F 'file=@morning_routine.bpmn' http://localhost:8080/deployment"
    Then the BPMN file should be deployed successfully

    When I start the morning routine workflow using the command "curl -X POST http://localhost:8080/process-definition/key/MorningRoutine/start"
    Then the morning routine workflow should be started

    When I confirm the task "Brush Teeth" using the command "curl -X POST http://localhost:8080/task/{taskId}/complete"
    Then the task "Brush Teeth" should be marked as complete

    When I check the status of the workflow using the command "curl -X GET http://localhost:8080/process-instance"
    Then I should see the current status of the workflow

    When I stop the workflow engine using the command "docker-compose down"
    Then the workflow engine should be stopped
