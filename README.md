---
- name: Execute chef-client and grep for a specific recipe
  hosts: your_targeted_hosts
  become: yes
  tasks:
    - name: Run chef-client
      command: chef-client
      register: chef_client_output
      ignore_errors: true  # Prevent playbook from stopping if chef-client fails

    - name: Check if specific recipe was applied
      shell: echo "{{ chef_client_output.stdout }}" | grep 'my_specific_recipe'
      register: grep_output
      ignore_errors: true

    - name: Print grep result
      debug:
        var: grep_output.stdout_lines
      when: grep_output.rc == 0  # Condition to check if grep found something
