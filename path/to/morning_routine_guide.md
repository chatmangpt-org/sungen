# Morning Routine Guide

## Overview
This guide outlines how to use a BPMN workflow engine to ensure you follow your morning routine. The system will send you a text message reminder if you do not confirm the completion of each task.

## Workflow Steps

1. **Wake Up**
   - Trigger: Start the workflow when you wake up.
   - Action: Send a text message asking you to confirm that you have woken up.

2. **Brush Teeth**
   - Trigger: Wait for a confirmation text message that you have brushed your teeth.
   - Action: If no confirmation is received within a specified time (e.g., 10 minutes), send a reminder text message.

3. **Take Shower**
   - Trigger: Wait for a confirmation text message that you have taken a shower.
   - Action: If no confirmation is received within a specified time (e.g., 10 minutes), send a reminder text message.

4. **Have Breakfast**
   - Trigger: Wait for a confirmation text message that you have had breakfast.
   - Action: If no confirmation is received within a specified time (e.g., 10 minutes), send a reminder text message.

5. **Ready for the Day**
   - Trigger: Once all tasks are confirmed, send a final text message congratulating you on completing your morning routine.

## Implementation
To implement this workflow, you will need:
- A BPMN workflow engine that supports sending text messages.
- A way to receive and process incoming text messages.

### Example BPMN Diagram
Refer to the `morning_routine.bpmn` file for a visual representation of the workflow.

### Example YAML Configuration
Refer to the `morning_routine.yaml` file for the configuration of the workflow.

## Conclusion
By following this guide and implementing the BPMN workflow, you can ensure that you complete your morning routine efficiently. The reminder system will help keep you accountable and on track.
