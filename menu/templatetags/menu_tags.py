from django import template

from menu.models import Item


register = template.Library()


def get_items_for_display(selected_item, all_items):
    items_for_display = list()
    current_item = selected_item

    if not current_item:
        return list(filter(is_primary, all_items))

    while current_item:
        children = list(filter_items(current_item, is_child, all_items))
        current_item.children = children

        if is_primary(current_item):
            items_for_display.append(current_item)
            items_for_display.extend(list(filter_items(current_item.id, is_primary, all_items)))
            break

        current_item = next(filter_items(current_item, is_parent, all_items), None)

    return items_for_display


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    result = {}
    all_items = list(Item.used.filter(menu__name=menu_name))
    selected_item_url = context['request'].path[1:-1]
    result['selected_item'] = next(filter_items(selected_item_url, is_selected, all_items), None)
    result['items_for_display'] = sorted(get_items_for_display(result['selected_item'], all_items),
                                         key=lambda item: item.id)
    return result


def filter_items(arg, condition, elements_set):
    return filter(lambda item: condition(item, arg), elements_set)


def is_selected(item, url):
    return item.url == url


def is_child(item, selected_item):
    return item.parent_id == selected_item.id


def is_parent(item, selected_item):
    return item.id == selected_item.parent_id


def is_primary(item, exclude_id=None):
    return item.parent_id is None and item.id != exclude_id
