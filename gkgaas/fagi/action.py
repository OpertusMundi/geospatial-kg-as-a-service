from enum import Enum


class FusionAction(Enum):
    # Keeps the value of the left source dataset in the fused model.
    KEEP_LEFT = 'keep-left'

    # same as "keep-left". The affected triples are added to the ambiguous
    # output.
    KEEP_LEFT_MARK_AMBIGUOUS = 'keep-left-mark-ambiguous'

    # Keeps the value of the right source dataset in the fused model.
    KEEP_RIGHT = 'keep-right'

    # Same as "keep-right". The affected triples ar4e added to the ambiguous
    # output.
    KEEP_RIGHT_MARK_MBIGUUS = 'keep-right-mark-ambiguous'

    # Keeps both values of thr source datasets as a concatenated literal in the
    # same property of the fused model.
    CONCATENATE = 'concatenate'

    # Same as "concatenate". The affected triples are added to the ambiguous
    # output.
    CONCATENATE_MARK_AMBIGUOUS = 'concatenate-mark-ambiguous'

    # Keeps the value of the longest literal in the fused model using the NFC
    # normalization before comparing the literals.
    KEEP_LONGEST = 'keep-longest'

    # Same as "keep-longest". The affected triples are added to the ambiguous
    # output.
    KEEP_LONGEST_MARK_AMBIGUOUS = 'keep-longest-mark-ambiguous'

    # Keeps the longest values of names with the same type (e.g. official,
    # international etc.). Regarding the names without a type it keeps the
    # longest value of each language. This action is supposed to work only for
    # name attributes.
    KEEP_MOST_COMPLETE_NAME = 'keep-most-complete-name'

    # Same as "keep-most-complete-name". The affected triples are added to the
    # ambiguous output.
    KEEP_MOST_COMPLETE_NAME_MARK_AMBIGUOUS = \
        'keep-most-complete-name-mark-ambiguous'

    # Keeps both values of the source datasets in a fused model.
    KEEP_BOTH = 'keep-both'

    # Same as "keep-both". The affected triples are added to th ambiguous
    # output.
    KEEP_BOTH_MARK_AMBIGUOUS = 'keep-both-mark-ambiguous'

    # Keeps the geometry that is composed of more points than the other
    KEEP_MORE_POINTS = 'keep-more-points'

    # Same as "keep-more-points". The affected triples are added to the
    # ambiguous output.
    KEEP_MORE_POINTS_MARK_AMBIGUOUS = 'keep-more-points-mark-ambiguous'

    # Keeps the geometry with more points and shifts its centroid to the
    # centroid of the other geometry.
    KEEP_MORE_POINTS_AND_SHIFT = 'keep-more-points-and-shift'

    # Same as "keep-more-points-and-shift". The affected triples are added to
    # the ambiguous output.
    KEEP_MORE_POINTS_AND_SHIFT_MARK_AMBIGUOUS = \
        'keep-more-points-and-shift-mark-ambiguous'

    # Shifts the geometry of the left source entity to the centroid of the
    # right.
    SHIFT_LEFT_GEOMETRY = 'shift-left-geometry'

    # Same as "shift-left-geometry". The affected triples are added to the
    # ambiguous output.
    SHIFT_LEFT_GEOMETRY_MARK_AMBIGUOUS = 'shift-left-geometry-mark-ambiguous'

    # Shifts the geometry of the right source entity to the centroid of the
    # left.
    SHIFT_RIGHT_GEOMETRY = 'shift-right-geometry'

    # Same as "shift-right-geometry". The affected triples are added to the
    # ambiguous output.
    SHIFT_RIGHT_GEOMETRY_MARK_AMBIGUOUS = 'shift-right-geometry-mark-ambiguous'

    # Utilizes the ML model in order to predict the action.
    KEEP_RECOMMENDED = 'keep-recommended'

    # Same as "keep-recommended". The affected triples are added to the
    # ambiguous output.
    KEEP_RECOMMENDED_MARK_AMBIGUOUS = 'keep-recommended-mark-ambiguous'

    def __str__(self) -> str:
        return self.value
