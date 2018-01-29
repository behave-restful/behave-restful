

def before_all(context):
    context.before_all_invoked = True


def before_feature(context, feature):
    context.before_feature_invoked = True

def before_scenario(context, scenario):
    context.before_scenario_invoked = True


def before_step(context, step):
    context.before_step_invoked = True


def before_tag(context, tag):
    context.before_tag_invoked = True
