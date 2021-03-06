# -*- coding: utf-8 -*-
# Copyright (c) 2014 by Ecreall under licence AGPL terms
# available on http://www.gnu.org/licenses/agpl.html

# licence: AGPL
# author: Amen Souissi

from pyramid.threadlocal import get_current_request

from substanced.util import get_oid

from dace.objectofcollaboration.principal.util import has_any_roles
from dace.processinstance.activity import InfiniteCardinality, ActionType
from dace.interfaces import (
    IProcessDefinition,
    IRuntime,
    IProcessDefinitionContainer,
    IProcess,
    IActivity,
    IBusinessAction)
from dace.processdefinition.processdef import ProcessDefinition
from dace.processdefinition.activitydef import ActivityDefinition
from dace.processdefinition.transitiondef import TransitionDefinition
from dace.processdefinition.eventdef import (
    StartEventDefinition,
    EndEventDefinition)
from dace.processdefinition.gatewaydef import (
    ParallelGatewayDefinition, ExclusiveGatewayDefinition)
from dace.objectofcollaboration.services.processdef_container import (
    process_definition)
from pontus.core import VisualisableElement


def relation_validationA(process, context):
    return True


def roles_validationA(process, context):
    return has_any_roles(roles=('Admin',))


def processsecurity_validationA(process, context):
    return True


def state_validationA(process, context):
    return True


class StatisticProcesses(InfiniteCardinality):

    context = IRuntime
    actionType = ActionType.automatic
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA

    def url(self, obj):
        query = {}
        try:
            actionuid = get_oid(self)
            query = {'action_uid': actionuid}
        except AttributeError:
            query = {'isstart': 'True'}

        query['coordinates'] = 'main'
        return get_current_request().resource_url(
               obj, '@@'+self.view_name,  query=query)


class SeeProcesses(InfiniteCardinality):

    context = IRuntime
    actionType = ActionType.automatic
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA


@process_definition(name='runtime_pd', id='runtime_pd')
class RuntimeProcessDefinition(ProcessDefinition, VisualisableElement):
    isUnique = True
    discriminator = 'DaceManager'

    def __init__(self, **kwargs):
        super(RuntimeProcessDefinition, self).__init__(**kwargs)
        self.title = 'Processus de gestion du runtime'
        self.description = "Ce processus permet de gérer les processus de l'application"

    def _init_definition(self):
        self.defineNodes(
                s = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                processes_run = ActivityDefinition(contexts=[SeeProcesses],
                                    title="Les processus en cours",
                                    groups=['Voir'],
                                    description="L'action permet de voir les processus en cours"),
                processes_stat = ActivityDefinition(contexts=[StatisticProcesses],
                                    title="Tableau de bord",
                                    groups=['Voir', 'Statistique'],
                                    description="L'action permet de voir les statistiques des processus en cours"),
                eg = ExclusiveGatewayDefinition(),
                e = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('s', 'pg'),
                TransitionDefinition('pg', 'processes_run'),
                TransitionDefinition('processes_run', 'eg'),
                TransitionDefinition('pg', 'processes_stat'),
                TransitionDefinition('processes_stat', 'eg'),
                TransitionDefinition('eg', 'e'),
        )


class SeeProcessesDef(InfiniteCardinality):

    context = IProcessDefinitionContainer
    actionType = ActionType.automatic
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA



@process_definition(name='pdc_pd', id='pdc_pd')
class PDCProcessDefinition(ProcessDefinition, VisualisableElement):
    isUnique = True
    discriminator = 'DaceManager'

    def __init__(self, **kwargs):
        super(PDCProcessDefinition, self).__init__(**kwargs)
        self.title = 'Processus de gestion du containeur des définitions des processus'
        self.description = "Ce processus permet de gerer le containeur des définitions des processus de l'application"

    def _init_definition(self):
        self.defineNodes(
                s = StartEventDefinition(),
                processes_def = ActivityDefinition(contexts=[SeeProcessesDef],
                                                   title="Les définitions des processus",
                                                   groups=['Voir'],
                                                   description="L'action permet de voir les définitions des processus"),
                e = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('s', 'processes_def'),
                TransitionDefinition('processes_def', 'e'),
        )


class SeeProcessDef(InfiniteCardinality):

    context = IProcessDefinition
    actionType = ActionType.automatic
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA


class StatisticProcessesDef(InfiniteCardinality):

    context = IProcessDefinition
    actionType = ActionType.automatic
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA

    def url(self, obj):
        query = {}
        try:
            actionuid = get_oid(self)
            query = {'action_uid': actionuid}
        except AttributeError:
            query = {'isstart': 'True'}

        query['coordinates'] = 'main'
        return get_current_request().resource_url(
             obj, '@@'+self.view_name,  query=query)

class InstanceProcessesDef(InfiniteCardinality):

    context = IProcessDefinition
    actionType = ActionType.automatic
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA


@process_definition(name='pd_pd', id='pd_pd')
class PDProcessDefinition(ProcessDefinition, VisualisableElement):
    isUnique = True
    discriminator = 'DaceManager'

    def __init__(self, **kwargs):
        super(PDProcessDefinition, self).__init__(**kwargs)
        self.title = 'Processus de gestion des définitions des processus'
        self.description = "Ce processus permet de gérer les définitions des processus de l'application"

    def _init_definition(self):
        self.defineNodes(
                s = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                processes_def = ActivityDefinition(contexts=[SeeProcessDef],
                                                   title="La définition de processus",
                                                   groups=['Voir'],
                                                   description="L'action permet de voir les détails de la definition de processus"),
                processes_stat = ActivityDefinition(contexts=[StatisticProcessesDef],
                                                   title="Tableau de bord",
                                                   groups=['Voir','Statistique'],
                                                   description="L'action permet de voir les statistiques des processus en cours"),

                processes_run = ActivityDefinition(contexts=[InstanceProcessesDef],
                                                   title="Les processus en cours",
                                                   groups=['Voir'],
                                                   description="L'action permet de voir les détails des processus en cours"),
                eg = ExclusiveGatewayDefinition(),
                e = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('s', 'pg'),
                TransitionDefinition('pg', 'processes_def'),
                TransitionDefinition('pg', 'processes_stat'),
                TransitionDefinition('pg', 'processes_run'),
                TransitionDefinition('processes_def', 'eg'),
                TransitionDefinition('processes_run', 'eg'),
                TransitionDefinition('processes_stat', 'eg'),
                TransitionDefinition('eg', 'e'),
        )



class SeeProcess(InfiniteCardinality):

    context = IProcess
    actionType = ActionType.automatic
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA


class StatisticProcess(InfiniteCardinality):

    context = IProcess
    actionType = ActionType.automatic
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA

    def url(self, obj):
        query = {}
        try:
            actionuid = get_oid(self)
            query = {'action_uid':actionuid}
        except AttributeError:
            query = {'isstart':'True'}

        query['coordinates'] = 'main'
        return get_current_request().resource_url(
             obj, '@@'+self.view_name,  query=query)


class SeeProcessDatas(InfiniteCardinality):

    context = IProcess
    actionType = ActionType.automatic
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA

class DoActivitiesProcess(InfiniteCardinality):

    context = IProcess
    actionType = ActionType.automatic
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA


@process_definition(name='p_pd', id='p_pd')
class PProcessDefinition(ProcessDefinition, VisualisableElement):
    isUnique = True
    discriminator = 'DaceManager'

    def __init__(self, **kwargs):
        super(PProcessDefinition, self).__init__(**kwargs)
        self.title = 'Processus de gestion des processus'
        self.description = "Ce processus permet de gérer les processus de l'application"

    def _init_definition(self):
        self.defineNodes(
                s = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                processes_def = ActivityDefinition(contexts=[SeeProcess],
                                                   title="Details",
                                                   groups=['Voir'],
                                                   description="L'action permet de voir les détails du processus"),
                processes_stat = ActivityDefinition(contexts=[StatisticProcess],
                                                   title="Tableau de bord",
                                                   groups=['Voir', 'Statistique'],
                                                   description="L'action permet de voir les statistiques du processus en cours"),
                processes_datas = ActivityDefinition(contexts=[SeeProcessDatas],
                                                   title="Les données manipulées",
                                                   groups=['Voir'],
                                                   description="L'action permet de voir les donnees manipulées par le processus"),
                processes_actions = ActivityDefinition(contexts=[DoActivitiesProcess],
                                                   title="Les actions a realiser",
                                                   groups=[],
                                                   description="L'action permet de réaliser les actions en relation avec le processus"),
                eg = ExclusiveGatewayDefinition(),
                e = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('s', 'pg'),
                TransitionDefinition('pg', 'processes_def'),
                TransitionDefinition('pg', 'processes_stat'),
                TransitionDefinition('pg', 'processes_datas'),
                TransitionDefinition('pg', 'processes_actions'),
                TransitionDefinition('processes_def', 'eg'),
                TransitionDefinition('processes_stat', 'eg'),
                TransitionDefinition('processes_datas', 'eg'),
                TransitionDefinition('processes_actions', 'eg'),
                TransitionDefinition('eg', 'e'),
        )


class AssignToUsers(InfiniteCardinality):

    isSequential = True
    context = IActivity
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA

    def start(self, context, request, appstruct, **kw):
        users = list(appstruct.pop('users'))
        context.set_assignment(users)
        return {}

class AssignActionToUsers(InfiniteCardinality):

    context = IBusinessAction
    relation_validation = relation_validationA
    roles_validation = roles_validationA
    processsecurity_validation = processsecurity_validationA
    state_validation = state_validationA

    def start(self, context, request, appstruct, **kw):
        users = list(appstruct.pop('users'))
        context.set_assignment(users)
        return {}


@process_definition(name='activity_pd', id='activity_pd')
class ActivityProcessDefinition(ProcessDefinition, VisualisableElement):
    isUnique = True
    discriminator = 'DaceManager'

    def __init__(self, **kwargs):
        super(ActivityProcessDefinition, self).__init__(**kwargs)
        self.title = "Processus de gestion des activitées d'un processus"
        self.description = "Ce processus permet de gérer les activités d'un processus"

    def _init_definition(self):
        self.defineNodes(
                s = StartEventDefinition(),
                pg = ParallelGatewayDefinition(),
                activity_ass = ActivityDefinition(contexts=[AssignToUsers],
                                                   title="Assigner l'activité",
                                                   groups=['Administration'],
                                                   description="L'action permet d'assigner l'activité à des utlisateurs"),
                action_ass = ActivityDefinition(contexts=[AssignActionToUsers],
                                                   title="Assigner l'action",
                                                   groups=['Administration'],
                                                   description="L'action permet d'assigner l'action à des utlisateurs"),
                eg = ExclusiveGatewayDefinition(),
                e = EndEventDefinition(),
        )
        self.defineTransitions(
                TransitionDefinition('s', 'pg'),
                TransitionDefinition('pg', 'activity_ass'),
                TransitionDefinition('pg', 'action_ass'),
                #TransitionDefinition('pg', 'processes_run'),
                TransitionDefinition('activity_ass', 'eg'),
                #TransitionDefinition('processes_run', 'eg'),
                TransitionDefinition('action_ass', 'eg'),
                TransitionDefinition('eg', 'e'),
        )
