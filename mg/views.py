from django.http import JsonResponse

from exchange.models import EquipLibrary


def add(request):
    equip_library_data = [
        dict(
            category=EquipLibrary.Category.Weapon.value,
            type="雙手劍",
            name="普錫杰勒雙手劍",
            profession="聖魂劍士,英雄,凱撒",
            stage_level=EquipLibrary.Stage.White.value
        ),
        dict(
            category=EquipLibrary.Category.Weapon.value,
            type="雙手劍",
            name="傑伊西恩雙手劍",
            profession="聖魂劍士,英雄,凱撒",
            stage_level=EquipLibrary.Stage.White.value
        ),
        dict(
            category=EquipLibrary.Category.Weapon.value,
            type="長槍",
            name="普錫杰勒之槍",
            profession="黑騎士",
            stage_level=EquipLibrary.Stage.White.value
        ),
        dict(
            category=EquipLibrary.Category.Weapon.value,
            type="長槍",
            name="傑伊希恩之槍",
            profession="黑騎士",
            stage_level=EquipLibrary.Stage.White.value
        ),
        dict(
            category=EquipLibrary.Category.Armor.value,
            type="帽子",
            name="伊克雷帝帽",
            profession="法師",
            stage_level=EquipLibrary.Stage.White.value
        ),
        dict(
            category=EquipLibrary.Category.Armor.value,
            type="帽子",
            name="伊克雷帝海王星帽",
            profession="海盜",
            stage_level=EquipLibrary.Stage.White.value
        ),
        dict(
            category=EquipLibrary.Category.Armor.value,
            type="套服",
            name="伊克雷帝勇士鎧甲",
            profession="劍士",
            stage_level=EquipLibrary.Stage.White.value
        ),
        dict(
            category=EquipLibrary.Category.Armor.value,
            type="套服",
            name="伊克雷帝奧丁神袍",
            profession="法師",
            stage_level=EquipLibrary.Stage.White.value
        ),
        dict(
            category=EquipLibrary.Category.Skins.value,
            type="武器",
            name="不漂釀捏",
        ),
        dict(
            category=EquipLibrary.Category.Skins.value,
            type="武器",
            name="培根武器",
        ),
        dict(
            category=EquipLibrary.Category.Consumables.value,
            type="椅子",
            name="充滿願望的紙飛機",
        ),
        dict(
            category=EquipLibrary.Category.Consumables.value,
            type="椅子",
            name="冰淇淋女王卡車",
        ),
        dict(
            category=EquipLibrary.Category.Cooperate.value,
            type="帽子",
            name="亞妮造型",
        ),
        dict(
            category=EquipLibrary.Category.Cooperate.value,
            type="帽子",
            name="克里斯卡造型",
        )
    ]

    equip_library_obj = [EquipLibrary(**data) for data in equip_library_data]
    EquipLibrary.objects.bulk_create(equip_library_obj)
    
    data = list(EquipLibrary.objects.all().values())
    return JsonResponse(data, safe=False)

def delete(request):
    EquipLibrary.objects.all().delete()
    data = list(EquipLibrary.objects.all().values())
    return JsonResponse(data, safe=False)
