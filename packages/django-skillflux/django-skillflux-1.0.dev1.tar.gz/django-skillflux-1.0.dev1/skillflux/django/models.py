# Copyright 2020 Dominik George <dominik.george@teckids.org>
# Copyright 2020 Philipp Stahl <philipp.stahl@teckids.org>
# Copyright 2020 Johannes Tobisch <johannes.tobisch@teckids.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data model for the SkillFlux method"""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Skill(models.Model):
    """A particular competence that a *participant* can hold.
    It is thoroughly described so that holding a skill ensures that
    the holding participant has a well-defined competence. Participants
    have a set of *achieved* skills (i.e. competences they already hold),
    and a set of *aspired* skills (i.e. competences they want to learn).
    """

    caption = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    parent = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="subskills")

    level_max = models.PositiveSmallIntegerField(null=True)


class SkillExperience(models.Model):
    """A skill a *participant* has achieved through a *transition*.
    When a new skill is achieved, the experience can be annotated with
    a *level*.
    """

    skillset = models.ForeignKey("SkillSet", on_delete=models.CASCADE)
    skill = models.ForeignKey("Skill", on_delete=models.CASCADE)

    level = models.PositiveSmallIntegerField(null=True)
    experience = models.TextField(blank=True)


class SkillSet(models.Model):
    """A collection of *skills* that are put into relation for some purpose.
    This is intentionally left open. For aspects of the SkillFlux method
    that rely on skillsets, carefully read the rest of the definitions.
    Skillsets can be split into *subsets*.
    """

    caption = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)

    skills = models.ManyToManyField("Skill", related_name="skillsets", through="SkillExperience")
    subsets = models.ManyToManyField("self", related_name="supersets")

    @property
    def all_skills(self):
        """Get all skills, including skills in subsets."""
        qs = self.skills

        for subset in self.subsets.all():
            if subset is not self:
                qs = qs.union(subset.skills)

        return qs.all()

    def __eq__(self, other):
        return set(self.all_skills) == set(other.all_skills)

    def __le__(self, other):
        return set(self.all_skills) <= set(other.all_skills)

    def __lt__(self, other):
        return set(self.all_skills) < set(other.all_skills)

    def __ge__(self, other):
        return set(self.all_skills) >= set(other.all_skills)

    def __gt__(self, other):
        return set(self.all_skills) > set(other.all_skills)

    def __ne__(self, other):
        return set(self.all_skills) != set(other.all_skills)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            self.subsets.add(other)
        elif isinstance(other, Skill):
            self.skills.add(other)
        else:
            raise TypeError("Only single skills and other skillsets can be added to a skillset.")

        self.save()
        return self


class Transition(models.Model):
    """An event that adds new skills to a *participant*'s *achieved* *skillset*.
    A transition has an *expected* skillset (i.e. which skills a participant
    should have achieved before attempting the transition) and a *promised*
    skillset (i.e. which skills a participant will have achieved after the
    transition). After a transition, a participant's achieved skillset will
    consists of the sum of their previously achieved skillset and the promised
    skillset of the transition. In which form the transition occurs is outside
    the scope of the SkillFlux method. In practice, transistions are linked to
    events, e.g. learning sessions of different formats.
    """

    caption = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    effort = models.PositiveSmallIntegerField(default=0)

    expected = models.ForeignKey(
        "SkillSet",
        on_delete=models.PROTECT,
        related_name="expected_by",
        default=SkillSet.objects.create,
    )
    promised = models.ForeignKey(
        "SkillSet",
        on_delete=models.PROTECT,
        related_name="promised_by",
        default=SkillSet.objects.create,
    )

    def fulfilled(self, skillset):
        """Check whether expectations are fulfilled by a skillset."""
        if isinstance(skillset, Participant):
            skillset = skillset.achieved
        return self.expected <= skillset

    def achieved(self, skillset):
        """Check whether all promised skills have been achieved in a skillset."""
        if isinstance(skillset, Participant):
            skillset = skillset.achieved
        return self.promised <= skillset


class TransitionExperience(models.Model):
    """A transition successfully attempted by a *participant*.
    Their experience should be documented in text form accompanying
    the transition.
    """

    participant = models.ForeignKey("Participant", on_delete=models.CASCADE)
    transition = models.ForeignKey("Transition", on_delete=models.CASCADE)

    caption = models.CharField(max_length=30, blank=True)
    experience = models.TextField(blank=True)


class Participant(models.Model):
    """Any entity partaking in the SkillFlux method.
    They have *achieved* a certain *skillset* (i.e. they hold a certain
    skillset at any time), and *aspire* a certain skillset (i.e. they have
    a goal they want to reach through the SkillFlux method). To reach that
    aspired skillset, they *experience* *transitions*.
    """

    user_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    user_id = models.PositiveIntegerField()
    user = GenericForeignKey("user_type", "user_id")

    achieved = models.ForeignKey(
        "SkillSet",
        on_delete=models.PROTECT,
        related_name="achieved_by",
        default=SkillSet.objects.create,
    )
    aspired = models.ForeignKey(
        "SkillSet",
        on_delete=models.PROTECT,
        related_name="aspired_by",
        default=SkillSet.objects.create,
    )

    def achieve(self, transition):
        """Achieve all skills a transition promises."""
        self.achieved += transition.promised
        self.achieved.save()

    def aspire(self, skillset):
        """Aspire a skillset by adding it as subset to the aspired skillset.."""
        self.aspired += skillset
        self.aspired.save()

    @property
    def experienced(self):
        """Get all transitions undergone to achieve the currently achieved skillset."""
        qs = self.achieved.promised_by

        for subset in self.achieved.subsets.all():
            qs = qs.union(subset.promised_by)

        return qs

    @property
    def fulfilled(self):
        """Get all transitions that this participant can experience."""
        transitions = Transition.objects.all()
        for transition in transitions:
            if transition.expected > self.achieved:
                transitions = transitions.exclude(transition)

        return transitions
