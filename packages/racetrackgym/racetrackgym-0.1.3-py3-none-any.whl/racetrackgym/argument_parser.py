from rlmate.argument_parser import Argument_parser


class Racetrack_parser(Argument_parser):
    def __init__(self):
        super().__init__()
        # Racetrack arguments
        # # RT needed
        self.parser.add_argument(
            "map_name", type=str, help="the map to run the racetrack on"
        )
        self.parser.add_argument(
            "-n",
            "--noise",
            help="use noisy version of racetrack",
            default=False,
            action="store_true",
        )
        self.parser.add_argument(
            "-rs",
            "--random_start",
            help="start racetrack from anywhere",
            default=False,
            action="store_true",
        )
        self.parser.add_argument(
            "-rv",
            "--random_velocity",
            help="start racetrack with random velocity",
            default=False,
            action="store_true",
        )
        self.parser.add_argument(
            "-l",
            "--landmarking",
            help="use landmarking. Requires a potential file",
            default=False,
            action="store_true",
        )
        self.parser.add_argument(
            "-sww",
            "--surround_with_walls",
            help="sorround map with walls",
            default=False,
            action="store_true",
        )
        self.parser.add_argument(
            "-ct",
            "--continuous",
            help="use continiuous version of rt",
            default=False,
            action="store_true",
        )

        # # RT binaries

        # # RT options
        self.parser.add_argument(
            "-nr",
            "--negative_reward",
            help="penalty when crashing",
            default=-20,
            type=float,
        )
        self.parser.add_argument(
            "-pr",
            "--positive_reward",
            help="reward when reaching the goal",
            default=100,
            type=float,
        )
        self.parser.add_argument(
            "-sr",
            "--step_reward",
            help="reward when doing an neutral step",
            default=0,
            type=float,
        )
        self.parser.add_argument(
            "-np",
            "--noise_probability",
            help="noise probability",
            default=0.1,
            type=float,
        )
        self.parser.add_argument(
            "-mrv",
            "--maximal_random_velocity",
            help="maximal probability used for rv",
            default=5,
            type=int,
        )
        self.parser.add_argument(
            "-wgl",
            "--width_goal_line",
            help="with of the goal line. Only applicable when spawning new lines",
            default=3,
            type=int,
        )

        self.rt_keys = [
            "hermes_name",
            "seed",
            "extract_all_states",
            "map_name",
            "noise",
            "random_start",
            "random_velocity",
            "landmarking",
            "surround_with_walls",
            "negative_reward",
            "positive_reward",
            "step_reward",
            "noise_probability",
            "maximal_random_velocity",
            "gamma",
            "continuous",
            "width_goal_line",
        ]
        self.spec_keys.append(self.rt_keys)
