from pathlib import Path
from typing import TYPE_CHECKING, Optional
from app.schemas.card_type import BaseCardModel

from modules.BaseCardType import (
    BaseCardType, ImageMagickCommands, Extra, CardDescription
)

if TYPE_CHECKING:
    from app.models.preferences import Preferences
    from modules.Font import Font


class DamonsTitleCard(BaseCardType):
    """
    This class describes a type of CardType that produces the 'generic'
    title cards based on Reddit user /u/UniversalPolymath. This card
    supports customization of every aspect of the card, but does not
    use any arbitrary data.
    """

    class CardModel(BaseCardModel):
        source_file: Path
        card_file: Path
        title_text: str
        episode_text: str
        hide_episode_text: bool = False
        season_text: str
        hide_season_text: bool = False
        font_color: str
        font_file: str
        font_interline_spacing: int
        font_interword_spacing: int
        font_kerning: float
        font_size: float
        font_stroke_width: float
        font_vertical_shift: int
        blur: bool = False
        grayscale: bool = False

    """API Parameters"""
    API_DETAILS = CardDescription(
        name='Damons Title Card',
        identifier='damon',
        example='/internal_assets/cards/standard.jpg',
        creators=['Damon Z'],
        source='local',
        supports_custom_fonts=True,
        supports_custom_seasons=False,
        supported_extras=[
            Extra(
                name='Gradient Omission',
                identifier='omit_gradient',
                description='Whether to omit the gradient overlay',
                tooltip=(
                    'Either <v>True</v> or <v>False</v>. If <v>True</v>, text '
                    'may appear less legible on brighter images.'
                ),
            ),
        ], description=[
            'Damons Title Card'
        ]
    )

    """Directory where all reference files used by this card are stored"""
    REF_DIRECTORY = BaseCardType.BASE_REF_DIRECTORY / 'olivier'
    SW_REF_DIRECTORY = BaseCardType.BASE_REF_DIRECTORY / 'star_wars'
    GRAD_REF_DIRECTORY = BaseCardType.BASE_REF_DIRECTORY

    """Characteristics for title splitting by this class"""
    TITLE_CHARACTERISTICS = {
        'max_line_width': 20,   # Character count to begin splitting titles
        'max_line_count': 4,    # Maximum number of lines a title can take up
        'top_heavy': True,      # This class uses top heavy titling
    }

    """Characteristics of the default title font"""
    TITLE_FONT = str((REF_DIRECTORY / 'Montserrat-Bold.ttf').resolve())
    TITLE_COLOR = '#EBEBEB'
    FONT_REPLACEMENTS = {}

    """Characteristics of the episode text"""
    EPISODE_TEXT_FORMAT = 'SEASON {to_cardinal(season_number)} • EPISODE {to_cardinal(episode_number)}'
    EPISODE_PREFIX_FONT = SW_REF_DIRECTORY / 'HelveticaNeue.ttc'
    EPISODE_NUMBER_FONT = SW_REF_DIRECTORY / 'HelveticaNeue-Bold.ttf'
    STROKE_COLOR = 'black'
    SERIES_COUNT_TEXT_COLOR = '#CFCFCF'

    """Source path for the gradient image"""
    __GRADIENT_IMAGE = GRAD_REF_DIRECTORY / 'GRADIENT.png'

    """Whether this class uses season titles for the purpose of archives"""
    USES_SEASON_TITLE = True

    """How to name archive directories for this type of card"""
    ARCHIVE_NAME = 'Damon Style'

    __slots__ = (
        'source_file', 'output_file', 'title_text', 'season_text',
        'episode_text', 'hide_season_text', 'hide_episode_text', 'font_color',
        'font_file', 'font_interline_spacing', 'font_interword_spacing', 'title_interline_spacing',
        'font_kerning', 'font_size', 'font_stroke_width', 'font_vertical_shift',
        'episode_text_color', 'omit_gradient', 'stroke_color', 
        'episode_text_font_size',
    )

    def __init__(self,
            source_file: Path,
            card_file: Path,
            title_text: str,
            season_text: str,
            episode_text: str,
            hide_season_text: bool = False,
            hide_episode_text: bool = False,
            font_color: str = TITLE_COLOR,
            font_file: str = TITLE_FONT,
            font_interline_spacing: int = 0,
            font_interword_spacing: int = 0,
            title_interline_spacing: int = -50,
            font_kerning: float = 1.0,
            font_size: float = 1.0,
            font_stroke_width: float = 1.0,
            font_vertical_shift: int = 0,
            blur: bool = False,
            grayscale: bool = False,
            stroke_color: str = 'black',
            episode_text_color: str = SERIES_COUNT_TEXT_COLOR,
            episode_text_font_size: float = 1.0,
            omit_gradient: bool = False,
            preferences: Optional['Preferences'] = None,
            **unused,
        ) -> None:
        """Construct a new instance of this card."""

        # Initialize the parent class - this sets up an ImageMagickInterface
        super().__init__(blur, grayscale, preferences=preferences)

        self.source_file = source_file
        self.output_file = card_file

        # Ensure characters that need to be escaped are
        self.title_text = self.image_magick.escape_chars(title_text)
        self.season_text = self.image_magick.escape_chars(season_text)
        self.episode_text = self.image_magick.escape_chars(episode_text)
        self.hide_season_text = hide_season_text
        self.hide_episode_text = hide_episode_text

        # Font/card customizations
        self.font_color = font_color
        self.font_file = font_file
        self.font_kerning = font_kerning
        self.font_interline_spacing = font_interline_spacing
        self.font_interword_spacing = font_interword_spacing
        self.title_interline_spacing = title_interline_spacing
        self.font_size = font_size
        self.font_stroke_width = font_stroke_width
        self.font_vertical_shift = font_vertical_shift

        # Optional extras
        self.omit_gradient = omit_gradient
        self.stroke_color = stroke_color
        self.episode_text_color = episode_text_color
        self.episode_text_font_size = episode_text_font_size



    @staticmethod
    def is_custom_font(font: 'Font', extras: dict) -> bool:
        """
        Determine whether the given font characteristics constitute a
        default or custom font.

        Args:
            font: The Font being evaluated.
            extras: Dictionary of extras for evaluation.

        Returns:
            True if a custom font is indicated, False otherwise.
        """

        custom_extras = (
            ('episode_text_color' in extras
                and extras['episode_text_color'] != DamonsTitleCard.SERIES_COUNT_TEXT_COLOR)
            or ('episode_text_font_size' in extras
                and extras['episode_text_font_size'] != 1.0)
            or ('stroke_color' in extras
                and extras['stroke_color'] != 'black')
        )

        return (custom_extras
            or ((font.color != DamonsTitleCard.TITLE_COLOR)
            or (font.file != DamonsTitleCard.TITLE_FONT)
            or (font.interline_spacing != 0)
            or (font.interword_spacing != 0)
            or (font.kerning != 1.0)
            or (font.size != 1.0)
            or (font.stroke_width != 1.0)
            or (font.vertical_shift != 0))
        )


    @staticmethod
    def is_custom_season_titles(
            custom_episode_map: bool,
            episode_text_format: str,
        ) -> bool:
        """
        Determine whether the given attributes constitute custom or
        generic season titles.

        Args:
            custom_episode_map: Whether the EpisodeMap was customized.
            episode_text_format: The episode text format in use.

        Returns:
            True if the episode map or episode text format is custom,
            False otherwise.
        """
        print(f'{custom_episode_map}')
        standard_etf = DamonsTitleCard.EPISODE_TEXT_FORMAT
        print(f'is_custom_season_titles: {episode_text_format != standard_etf}')
        return episode_text_format != standard_etf




    @property
    def format_text_commands(self) -> ImageMagickCommands:
        """Add All Text"""

        # Font customizations
        title_font_size = 200 * self.font_size
        episode_font_size = 90 * self.episode_text_font_size
        
        title_stroke_width = 12
        episode_stroke_width = 2
        
        episode_kerning = 10 * self.episode_text_font_size
        title_kerning = 0.5 * self.font_kerning
        
        interline_spacing = self.title_interline_spacing + self.font_interline_spacing
        interword_spacing = 50 + self.font_interword_spacing

        top_line, season_prefix, season_number, separator, episode_prefix, episode_number = ("",)*6
        try:
            season_prefix, season_number, separator, episode_prefix, episode_number = self.episode_text.upper().split(' ', 4)
        except:
            top_line = self.episode_text.upper()

        season_commands = []
        separator_commands = []
        episode_commands = []
        print(f'Hide Season Text: {self.hide_season_text}')
        print(f'Hide Episode Text: {self.hide_episode_text}')
        print(f'Top Line: {top_line}')
        if top_line.__len__() <= 0:
            # Standard Case with Season and Episode
            
            if not self.hide_season_text:
                if season_number == "ZERO":
                    season_commands = [
                        f'-font "{self.EPISODE_NUMBER_FONT.resolve()}"',
                        f'label:"SPECIAL"',
                    ]
                    self.hide_episode_text = True
                else: 
                    season_commands = [
                        f'-font "{self.EPISODE_PREFIX_FONT.resolve()}"',
                        f'label:"{season_prefix}"',
                        f'-font "{self.EPISODE_NUMBER_FONT.resolve()}"',
                        f'label:"{season_number}"',
                    ]
            
            if (not self.hide_season_text) and (not self.hide_episode_text):
                separator_commands = [
                    f'label:"{separator}"',
                ]
                    
            if not self.hide_episode_text:
                episode_commands = [
                    f'-font "{self.EPISODE_PREFIX_FONT.resolve()}"',
                    f'label:"{episode_prefix}"',
                    f'-font "{self.EPISODE_NUMBER_FONT.resolve()}"',
                    f'label:"{episode_number}"',
                ]


        return [
            f'-gravity west',

            # All Text
            f'\(',
            
            # Season & Episode
            f'\(',
            f'-gravity west',
            f'-fill "{self.SERIES_COUNT_TEXT_COLOR}"',
            f'-pointsize {episode_font_size}',
            f'-kerning {episode_kerning}',
            f'-stroke "{self.stroke_color}"',
            f'-strokewidth {episode_stroke_width}',
            *season_commands,
            *separator_commands,
            *episode_commands,
            f'+smush 40',
            f'\)',
            
            # Main Text
            f'\(',
            f'-gravity west',
            
            # Main Text Stroke
            f'-fill "{self.stroke_color}"',
            f'-font "{self.font_file}"',
            f'-kerning {title_kerning}',
            f'-pointsize {title_font_size}',
            f'-interline-spacing {interline_spacing}',
            f'-interword-spacing {interword_spacing}',
            f'-stroke "{self.stroke_color}"',
            f'-strokewidth {title_stroke_width}',
            f'label:"{self.title_text}"',
            # f'-geometry +4',

            # Main Text 
            f'-fill "{self.font_color}"',
            f'-font "{self.font_file}"',
            f'-kerning {title_kerning}',
            f'-pointsize {title_font_size}',
            f'-interline-spacing {interline_spacing}',
            f'-interword-spacing {interword_spacing}',
            f'-stroke "{self.font_color}"',
            f'-strokewidth 0',
            f'label:"{self.title_text}"',
            
            # Combine Main Text and Stroke
            f'-composite',
            f'\)',

            # Combine Season, Episode & Main Text
            f'-gravity west',
            f'-smush 50',
            f'\)',

            f'-gravity southwest',
            f'-geometry +150+100',
            f'-composite',
        ]
    


    @property
    def gradient_command(self) -> ImageMagickCommands:
        """Subcommand to add Gradient"""
        
        # Sub-command to optionally add gradient
        ret = []
        if not self.omit_gradient:
            ret = [
                f'"{self.__GRADIENT_IMAGE.resolve()}"',
                f'-composite',
            ]
        
        return ret

    def create(self) -> None:
        """
        Make the necessary ImageMagick and system calls to create this
        object's defined title card.
        """

        command = ' '.join([
            f'convert "{self.source_file.resolve()}"',
            # Resize and optionally blur source image
            *self.resize_and_style,
            # Overlay gradient
            *self.gradient_command,
            *self.format_text_commands,
            *self.resize_output,
            f'"{self.output_file.resolve()}"',
        ])
        # sys.stdout.write(f"command: {command}")
        print(f"command: {command}")
        

        self.image_magick.run(command)
