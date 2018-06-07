import datetime
import json
# import os.path
import re

import click
from PyOrgMode import PyOrgMode


def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'

    Cribbed from django project: 
    https://github.com/django/django/blob/ce3351b9508896afdf87d11bd64fd6b5ad928228/django/utils/text.py#L223-L233
    
    Copyright (c) Django Software Foundation and individual contributors.
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification,
    are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Django nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def nozbe_name_to_org_filename(org_mode_dir, name):
    """
    Return an appropriate org-mode filename given a nozbe project name and org-mode directory.
    """
    return '%s/%s.org' % (org_mode_dir, get_valid_filename(name))


def nozbe_task_comments(task):
    """
    Generator to yield each "line" of comments from a nozbe task
    """
    for task_comment in task['comments']:
        if not task_comment['deleted']:
            if type(task_comment['body']) == str:
                yield task_comment['body']
            elif type(task_comment['body']) == list:
                for x in task_comment['body']:
                    yield x['name']
            else:
                raise ValueError(str(task_comment))


def nozbe_task_to_org_mode_status(task):
    """
    Compute org-mode status for a nozbe task
    """
    return {
        True: 'DONE',           # TODO I don't see any DONE
        False: 'TODO',
    }[task['completed']]


def nozbe_task_to_org_mode_deadline(task):
    """
    Compute org-mode deadline string for a nozbe task, None if no deadline
    """
    if task['datetime'] is None:
        return None
    dt = datetime.datetime.strptime(task['datetime'], '%Y-%m-%d %H:%M:%S')
    return '<%s>' % dt.strftime('%Y-%m-%d %a')


@click.command()
@click.argument('nozbe_data_file', type=click.File('r'))
@click.argument('org_mode_dir', type=click.Path(exists=True))
def nozbe_to_org_mode(nozbe_data_file, org_mode_dir):
    """
    Read a nozbe data file and export to org-mode files
    """
    nozbe_data = json.load(nozbe_data_file)
    projects = {}
    # Process nozbe projects, constructing org-mode objects
    # project: [{ id, name }]
    for project in nozbe_data['project']:
        id = project['id']
        name = project['name']
        filename = nozbe_name_to_org_filename(org_mode_dir, name)
        org = PyOrgMode.OrgDataStructure()
        # TODO(Later) mutate instead of overwrite
        # if os.path.isfile(filename):
        #     org.load_from_file(filename)
        projects[id] = {
            'name': name,
            'filename': filename,
            'org': org
        }
    # Process nozbe tasks, writing to org structures
    # task: [{ id, project_id, name, comments: [{body (str or [{name}]), deleted}]}]
    for task in nozbe_data['task']:
        id = task['id']
        project_id = task['project_id']
        name = task['name']
        org = projects[project_id]['org']
        # basic todo
        todo = PyOrgMode.OrgNode.Element()
        todo.heading = name
        todo.level = 1
        todo.todo = nozbe_task_to_org_mode_status(task)
        # comments
        for heading in nozbe_task_comments(task):
            comment = PyOrgMode.OrgNode.Element()
            comment.heading = heading
            comment.level = todo.level + 1
            todo.append_clean(comment)
        # deadline
        deadline = nozbe_task_to_org_mode_deadline(task)
        if deadline is not None:
            sched = PyOrgMode.OrgSchedule()
            sched._append(todo, sched.Element(deadline=deadline))
        # props
        props = PyOrgMode.OrgDrawer.Element("PROPERTIES")
        # nozbe id for future TODO of mutating rather than overwriting file
        props.append(PyOrgMode.OrgDrawer.Property("NOZBE_TASK_ID", id))
        todo.append_clean(props)
        org.root.append_clean(todo)
    # Save org-mode objects to files
    for project in projects.values():
        org = project['org']
        filename = project['filename']
        org.save_to_file(filename)


if __name__ == '__main__':
    nozbe_to_org_mode()
