import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()
from django.db.models import Q, Count, F, Sum, Avg
from main_app.models import Astronaut, Mission, Spacecraft


# Import your models here

# Create queries within functions

def get_astronauts(search_string=None):
    if search_string is None:
        return ""

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts:
        return ""

    result = ""
    for astronaut in astronauts:
        status = "Active" if astronaut.is_active else "Inactive"
        result += f"Astronaut: {astronaut.name}, phone number: {astronaut.phone_number}, status: {status}\n"

    return result.strip()


def get_top_astronaut():
    astronauts = Astronaut.objects.annotate(num_missions=Count('mission')).order_by('-num_missions', 'phone_number')

    if not astronauts or astronauts[0].num_missions == 0:
        return "No data."

    top_astronaut = astronauts[0]
    return f"Top Astronaut: {top_astronaut.name} with {top_astronaut.num_missions} missions."


def get_top_commander():
    astronauts = Astronaut.objects.annotate(num_commanded_missions=Count('commanded_missions')).order_by(
        '-num_commanded_missions', 'phone_number')

    if not astronauts or astronauts[0].num_commanded_missions == 0:
        return "No data."

    top_commander = astronauts[0]
    return f"Top Commander: {top_commander.name} with {top_commander.num_commanded_missions} commanded missions."


def get_last_completed_mission():
    mission = Mission.objects.filter(status='Completed').order_by('-launch_date').first()

    if not mission:
        return "No data."

    commander_name = mission.commander.name if mission.commander else "TBA"
    astronauts = mission.astronauts.order_by('name')
    astronaut_names = ', '.join(astronaut.name for astronaut in astronauts)
    total_spacewalks = astronauts.aggregate(total=Sum('spacewalks'))['total'] or 0

    return (f"The last completed mission is: {mission.name}. Commander: {commander_name}. "
            f"Astronauts: {astronaut_names}. Spacecraft: {mission.spacecraft.name}. "
            f"Total spacewalks: {total_spacewalks}.")


def get_most_used_spacecraft():
    spacecraft = (Spacecraft.objects
                  .annotate(num_missions=Count('mission'))
                  .order_by('-num_missions', 'name')
                  .first())

    if not spacecraft or spacecraft.num_missions == 0:
        return "No data."

    num_astronauts = (Astronaut.objects
                      .filter(mission__spacecraft=spacecraft)
                      .distinct()
                      .count())

    return (f"The most used spacecraft is: {spacecraft.name}, manufactured by {spacecraft.manufacturer}, "
            f"used in {spacecraft.num_missions} missions, astronauts on missions: {num_astronauts}.")


def decrease_spacecrafts_weight():
    spacecrafts = (Spacecraft.objects
                   .filter(mission__status='Planned', weight__gte=200.0)
                   .distinct())

    if not spacecrafts.exists():
        return "No changes in weight."

    num_of_spacecrafts_affected = spacecrafts.count()

    for spacecraft in spacecrafts:
        spacecraft.weight = F('weight') - 200.0
        spacecraft.save()

    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    return (f"The weight of {num_of_spacecrafts_affected} spacecrafts has been decreased. "
            f"The new average weight of all spacecrafts is {avg_weight:.1f}kg")

