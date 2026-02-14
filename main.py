# -*- coding: utf-8 -*-
import os
import json
import webbrowser
import threading
from pathlib import Path
import sys
import io

# Kivy 설정
from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')
Config.set('graphics', 'resizable', False)  # 크기 고정

# 한글 인코딩 설정 - 오류 무시
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
except:
    pass  # 컴퓨터 IDLE 등에서는 무시

# 나머지 임포트
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.utils import platform
from functools import lru_cache

# Kivy 한글 폰트 설정
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path

# 안드로이드 환경 확인
IS_ANDROID = platform == 'android'

# 안드로이드 저장소 경로 최적화
if IS_ANDROID:
    try:
        from android.storage import app_storage_path
        from android.permissions import request_permissions, Permission
        
        # 권한 요청
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        
        # 앱 전용 저장소 사용 (안드로이드 11+ 호환성)
        DATA_DIR = Path(app_storage_path()) / 'data'
    except:
        # 폴백: 외부 저장소
        from android.storage import primary_external_storage_path
        storage_path = primary_external_storage_path()
        DATA_DIR = Path(storage_path) / 'sannaeeum'
else:
    DATA_DIR = Path.cwd() / 'data'

# 데이터 디렉토리 생성
DATA_DIR.mkdir(exist_ok=True, parents=True)

# ============================================================
# 마루부리 폰트 설정
# ============================================================
FONT_NAME = 'MaruBuri'
FONT_PATH = 'res/fonts/MaruBuri-Bold.ttf'
KOREAN_FONT_AVAILABLE = False

# 폰트 등록 시도
try:
    if os.path.exists(FONT_PATH):
        font_dir = os.path.dirname(FONT_PATH)
        if font_dir:
            resource_add_path(font_dir)
        
        font_file = os.path.basename(FONT_PATH)
        LabelBase.register(name=FONT_NAME, fn_regular=font_file)
        KOREAN_FONT_AVAILABLE = True
        print(f"✅ 마루부리 폰트 등록 성공: {FONT_PATH}")
    else:
        print(f"⚠️ 마루부리 폰트를 찾을 수 없습니다: {FONT_PATH}")
        
        if IS_ANDROID:
            system_fonts = [
                '/system/fonts/NotoSansCJK-Regular.ttc',
                '/system/fonts/NotoSansKR-Regular.otf',
                '/system/fonts/DroidSansFallback.ttf'
            ]
            for sys_font in system_fonts:
                if os.path.exists(sys_font):
                    resource_add_path(os.path.dirname(sys_font))
                    LabelBase.register(name=FONT_NAME, fn_regular=os.path.basename(sys_font))
                    KOREAN_FONT_AVAILABLE = True
                    print(f"✅ 시스템 폰트로 대체: {sys_font}")
                    break
except Exception as e:
    print(f"⚠️ 폰트 등록 실패: {e}")
    KOREAN_FONT_AVAILABLE = False

def get_font_name():
    """사용 가능한 폰트 이름 반환"""
    return FONT_NAME if KOREAN_FONT_AVAILABLE else None

# ============================================================
# 색상 정의
# ============================================================
COLORS = {
    'primary': '#8B5FBF',
    'primary_light': '#9D76C7',
    'primary_dark': '#6A4A8C',
    'secondary': '#D4BFFF',
    'accent': '#C8A2C8',
    'danger': '#FF6B6B',
    'warning': '#FFA726',
    'success': '#66BB6A',
    'green': '#2E7D32',
    'gold': '#FFD700',
    'background': '#F5F0FF',
    'text_primary': '#2D1B4E',
    'text_secondary': '#5D4A7A',
    'white': '#FFFFFF',
    'pink': '#FF69B4',
    'link_blue': '#1E40AF',
    'category_text': '#4C1D95',
    'description_text': '#2D1B4E'
}

# 분류 카테고리 정의
CATEGORIES = {
    '0': '분류안함',
    '1': '교육',
    '2': '아이디어',
    '3': '생활',
    '4': '농업',
    '5': '쇼핑',
    '6': '여행',
    '7': '비즈니스',
    '8': '건강',
    '9': '가정',
    '10': '커뮤니티'
}

def hex_to_rgb(hex_color, alpha=1.0):
    """16진수 색상을 RGB 튜플로 변환"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return (r, g, b, alpha)
    return (1, 1, 1, 1)

# ============================================================
# 커스텀 위젯 클래스들
# ============================================================

class SimplePromotionButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = hex_to_rgb(COLORS['pink'])
        self.color = hex_to_rgb(COLORS['white'])
        self.size_hint_y = None
        self.height = dp(55)
        self.font_size = dp(20)
        self.bold = True
        self.padding = [dp(15), dp(10)]
        self.font_name = get_font_name()

class SimpleTitleLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(10)
        self.spacing = dp(5)
        
        with self.canvas.before:
            Color(*hex_to_rgb(COLORS['primary']))
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.title_label = Label(
            text='산내음 링크 관리자',
            font_size=dp(24),
            bold=True,
            color=hex_to_rgb(COLORS['white']),
            size_hint_y=None,
            height=dp(60),
            font_name=get_font_name()
        )
        
        self.add_widget(self.title_label)
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PurpleButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = hex_to_rgb(COLORS['primary'])
        self.color = hex_to_rgb(COLORS['white'])
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = dp(16)
        self.bold = True
        self.font_name = get_font_name()

class SmallButton(Button):
    def __init__(self, color_type='primary', **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.size_hint = (None, None)
        self.size = (dp(40), dp(40))
        self.font_size = dp(12)
        self.color = hex_to_rgb(COLORS['white'])
        
        if color_type == 'danger':
            self.background_color = hex_to_rgb(COLORS['danger'])
        elif color_type == 'warning':
            self.background_color = hex_to_rgb(COLORS['warning'])
        elif color_type == 'success':
            self.background_color = hex_to_rgb(COLORS['success'])
        else:
            self.background_color = hex_to_rgb(COLORS['primary'])
        
        self.font_name = get_font_name()

class CategoryToggleButton(ToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = hex_to_rgb(COLORS['secondary'])
        self.background_color_down = hex_to_rgb(COLORS['primary'])
        self.color = hex_to_rgb(COLORS['text_primary'])
        self.size_hint_y = None
        self.height = dp(30)
        self.font_size = dp(12)
        self.group = 'categories'
        self.font_name = get_font_name()

class LinkCard(BoxLayout):
    def __init__(self, title, description, url, category, index, delete_callback, edit_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.padding = [dp(15), dp(10), dp(5), dp(10)]
        self.spacing = dp(8)
        self.title = title
        self.url = url
        self.category = category
        self.index = index
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        
        # 카드 전체 배경
        with self.canvas.before:
            Color(*hex_to_rgb(COLORS['secondary'], 0.8))
            self.rect = RoundedRectangle(
                radius=[dp(15)] * 4,
                size=self.size,
                pos=self.pos
            )
        
        # 카드 내용 (좌측)
        content_layout = BoxLayout(orientation='vertical', size_hint=(0.65, 1))
        
        font_name = get_font_name()
        
        # 제목
        title_label = Label(
            text=title,
            size_hint_y=None,
            height=dp(30),
            color=hex_to_rgb(COLORS['text_primary']),
            font_size=dp(18),
            bold=True,
            text_size=(None, None),
            halign='left',
            font_name=font_name
        )
        title_label.bind(texture_size=title_label.setter('size'))
        
        # 사이트 설명
        desc_label = Label(
            text=description,
            size_hint_y=None,
            color=hex_to_rgb(COLORS['text_primary']),
            font_size=dp(14),
            text_size=(dp(350), None),
            halign='left',
            valign='top',
            font_name=font_name
        )
        desc_label.bind(
            texture_size=lambda instance, value: setattr(instance, 'height', max(value[1], dp(40)))
        )
        
        # URL
        short_url = url[:50] + "..." if len(url) > 50 else url
        url_label = Label(
            text=short_url,
            size_hint_y=None,
            height=dp(20),
            color=hex_to_rgb(COLORS['link_blue']),
            font_size=dp(12),
            text_size=(None, None),
            halign='left',
            font_name=font_name
        )
        url_label.bind(texture_size=url_label.setter('size'))
        
        content_layout.add_widget(title_label)
        content_layout.add_widget(desc_label)
        content_layout.add_widget(url_label)
        
        # 카테고리 및 버튼 레이아웃 (우측)
        right_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), spacing=dp(5))
        
        # 카테고리 표시
        category_label = Label(
            text=CATEGORIES.get(category, '분류안함'),
            size_hint_y=None,
            height=dp(25),
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(13),
            bold=True,
            text_size=(None, None),
            halign='center',
            valign='middle',
            font_name=font_name
        )
        
        # 카테고리 배경
        with category_label.canvas.before:
            Color(*hex_to_rgb(COLORS['primary_dark']))
            self.category_bg = RoundedRectangle(
                radius=[dp(5)] * 4,
                size=category_label.size,
                pos=category_label.pos
            )
        
        category_label.bind(pos=self.update_category_bg, size=self.update_category_bg)
        
        # 버튼 레이아웃
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(5))
        
        edit_btn = SmallButton(color_type='warning', text='✎')
        edit_btn.bind(on_press=self.edit_link)
        
        delete_btn = SmallButton(color_type='danger', text='X')
        delete_btn.bind(on_press=self.delete_link)
        
        button_layout.add_widget(edit_btn)
        button_layout.add_widget(delete_btn)
        
        right_layout.add_widget(category_label)
        right_layout.add_widget(button_layout)
        
        self.add_widget(content_layout)
        self.add_widget(right_layout)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        Clock.schedule_once(self.calculate_height, 0.1)
    
    def calculate_height(self, dt):
        """내용에 따라 카드 높이를 동적으로 계산"""
        base_height = self.padding[1] + self.padding[3] + self.spacing * 2
        
        content_height = 0
        if len(self.children) > 0:
            content_layout = self.children[1]
            for child in content_layout.children:
                content_height += child.height
        
        right_height = 0
        if len(self.children) > 0:
            right_layout = self.children[0]
            for child in right_layout.children:
                right_height += child.height
            right_height += right_layout.spacing * (len(right_layout.children) - 1)
        
        final_height = max(content_height, right_height) + base_height
        self.height = max(final_height, dp(100))
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def update_category_bg(self, *args):
        if hasattr(self, 'category_bg'):
            self.category_bg.pos = self.children[0].children[1].pos
            self.category_bg.size = self.children[0].children[1].size
    
    def delete_link(self, instance):
        self.delete_callback(self.index)
    
    def edit_link(self, instance):
        self.edit_callback(self.index)
    
    def on_touch_down(self, touch):
        if len(self.children) > 0 and self.children[1].collide_point(*touch.pos):
            self.open_url_safe(self.url)
            return True
        return super().on_touch_down(touch)
    
    def open_url_safe(self, url):
        """비동기로 URL 열기 (UI 블로킹 방지)"""
        def _open():
            try:
                webbrowser.open(url)
            except Exception as e:
                Logger.error(f'LinkCard: URL 열기 실패: {e}')
        threading.Thread(target=_open).start()

# ============================================================
# 메인 앱 클래스
# ============================================================

class LinkApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(20)
        self.spacing = dp(20)
        self.links = []
        self.displayed_links = []
        self.data_file = DATA_DIR / 'links.json'
        self.current_sort = 'title_asc'
        self.search_mode = False
        self.selected_category = 'all'
        self._exit_pressed = False
        
        # 페이징 처리 (메모리 최적화)
        self.current_page = 0
        self.page_size = 20
        
        # 지연 초기화
        Clock.schedule_once(self.load_links, 0.1)
        Clock.schedule_once(self.setup_ui, 0.2)
        Clock.schedule_once(self.refresh_link_list, 0.3)
    
    def load_links(self, dt=None):
        """데이터 로드"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    loaded_links = json.load(f)
                    for link in loaded_links:
                        if 'category' not in link:
                            link['category'] = '0'
                    self.links = loaded_links
        except Exception as e:
            Logger.error(f'링크 로드 실패: {e}')
            self.links = []
    
    def setup_ui(self, dt=None):
        """UI 설정"""
        self.setup_promotion_buttons()
        
        title_layout = SimpleTitleLayout()
        self.add_widget(title_layout)
        
        self.setup_search_sort_ui()
        
        add_button = PurpleButton(text='+ 새 링크 추가')
        add_button.bind(on_press=self.show_add_link_popup)
        self.add_widget(add_button)
        
        self.setup_link_list()
    
    def setup_promotion_buttons(self):
        promotion_layout = BoxLayout(
            size_hint_y=None, 
            height=dp(60),
            spacing=dp(10),
            padding=[dp(5), dp(5), dp(5), dp(5)]
        )
        
        left_promo_btn = SimplePromotionButton(text='산내음청결고춧가루')
        left_promo_btn.bind(on_press=lambda x: self.open_url_safe('https://naver.me/5NqKupAN'))
        
        right_promo_btn = SimplePromotionButton(text='풀밭청결고춧가루')
        right_promo_btn.bind(on_press=lambda x: self.open_url_safe('https://naver.me/xaf7s1s5'))
        
        promotion_layout.add_widget(left_promo_btn)
        promotion_layout.add_widget(right_promo_btn)
        
        self.add_widget(promotion_layout)
    
    def open_url_safe(self, url):
        """비동기로 URL 열기"""
        def _open():
            try:
                webbrowser.open(url)
            except Exception as e:
                Logger.error(f'URL 열기 실패: {e}')
        threading.Thread(target=_open).start()
    
    def setup_search_sort_ui(self):
        font_name = get_font_name()
        
        search_category_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        self.search_input = TextInput(
            hint_text='검색어 (OR, AND, NOT 사용 가능, 예: 바람 OR 김)',
            size_hint=(0.5, 1),
            background_color=hex_to_rgb(COLORS['white']),
            foreground_color=hex_to_rgb(COLORS['text_primary']),
            font_name=font_name
        )
        
        self.category_btn = Button(
            text='전체포함',
            size_hint=(0.15, 1),
            background_color=hex_to_rgb(COLORS['primary_light']),
            font_name=font_name
        )
        self.category_btn.bind(on_press=self.show_category_popup)
        
        search_btn = Button(
            text='검색',
            size_hint=(0.1, 1),
            background_color=hex_to_rgb(COLORS['primary']),
            font_name=font_name
        )
        search_btn.bind(on_press=self.search_links)
        
        clear_btn = Button(
            text='전체',
            size_hint=(0.1, 1),
            background_color=hex_to_rgb(COLORS['accent']),
            font_name=font_name
        )
        clear_btn.bind(on_press=self.clear_search)
        
        search_category_layout.add_widget(self.search_input)
        search_category_layout.add_widget(self.category_btn)
        search_category_layout.add_widget(search_btn)
        search_category_layout.add_widget(clear_btn)
        
        sort_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5))
        
        sort_buttons = [
            ('제목↑', 'title_asc'),
            ('제목↓', 'title_desc'),
            ('주소↑', 'url_asc'),
            ('주소↓', 'url_desc')
        ]
        
        for text, sort_type in sort_buttons:
            btn = Button(
                text=text,
                size_hint=(0.25, 1),
                background_color=hex_to_rgb(COLORS['primary_light']),
                font_name=font_name
            )
            btn.bind(on_press=lambda x, st=sort_type: self.sort_links(st))
            sort_layout.add_widget(btn)
        
        self.add_widget(search_category_layout)
        self.add_widget(sort_layout)
    
    def show_category_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        content.size_hint = (1, 1)
        
        font_name = get_font_name()
        
        title_label = Label(
            text='분류 선택',
            size_hint_y=None,
            height=dp(40),
            color=hex_to_rgb(COLORS['text_primary']),
            font_size=dp(18),
            bold=True,
            font_name=font_name
        )
        content.add_widget(title_label)
        
        scroll = ScrollView(do_scroll_x=False)
        category_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        category_layout.bind(minimum_height=category_layout.setter('height'))
        
        all_btn = CategoryToggleButton(text='전체 포함')
        all_btn.bind(on_press=lambda x: self.select_category('all'))
        if self.selected_category == 'all':
            all_btn.state = 'down'
        category_layout.add_widget(all_btn)
        
        for cat_id, cat_name in CATEGORIES.items():
            btn = CategoryToggleButton(text=f'{cat_id}. {cat_name}')
            btn.bind(on_press=lambda x, cid=cat_id: self.select_category(cid))
            if self.selected_category == cat_id:
                btn.state = 'down'
            category_layout.add_widget(btn)
        
        category_layout.height = len(CATEGORIES) * dp(35) + dp(40)
        scroll.add_widget(category_layout)
        content.add_widget(scroll)
        
        close_btn = Button(
            text='닫기',
            size_hint_y=None,
            height=dp(40),
            background_color=hex_to_rgb(COLORS['accent']),
            font_name=font_name
        )
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True
        )
        popup.open()
    
    def select_category(self, category_id):
        self.selected_category = category_id
        if category_id == 'all':
            self.category_btn.text = '전체포함'
        else:
            self.category_btn.text = f"{category_id}. {CATEGORIES.get(category_id, '분류안함')}"
        
        for child in self.children:
            if isinstance(child, Popup):
                child.dismiss()
                break
        
        self.refresh_link_list()
    
    def setup_link_list(self):
        self.scroll = ScrollView(do_scroll_x=False)
        self.link_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(15),
            padding=dp(10)
        )
        self.link_layout.bind(minimum_height=self.link_layout.setter('height'))
        
        self.scroll.add_widget(self.link_layout)
        self.add_widget(self.scroll)
    
    def refresh_link_list(self, dt=None):
        """링크 목록 새로고침 (페이징 적용)"""
        font_name = get_font_name()
        
        self.link_layout.clear_widgets()
        self.link_layout.height = 0
        
        links_to_display = self.displayed_links if self.search_mode else self.links
        
        if self.selected_category != 'all':
            links_to_display = [link for link in links_to_display if link.get('category', '0') == self.selected_category]
        
        if not links_to_display:
            empty_text = '검색 결과가 없습니다.' if self.search_mode else '저장된 링크가 없습니다.\n"새 링크 추가" 버튼을 눌러 추가하세요!'
            empty_label = Label(
                text=empty_text,
                size_hint_y=None,
                height=dp(100),
                color=hex_to_rgb(COLORS['text_secondary']),
                font_size=dp(16),
                halign='center',
                font_name=font_name
            )
            self.link_layout.add_widget(empty_label)
            self.link_layout.height += dp(100)
        else:
            # 페이징 처리
            start = self.current_page * self.page_size
            end = min(start + self.page_size, len(links_to_display))
            page_links = links_to_display[start:end]
            
            for i, link in enumerate(page_links):
                original_index = self.links.index(link) if link in self.links else (start + i)
                card = LinkCard(
                    link['title'], 
                    link['description'], 
                    link['url'], 
                    link.get('category', '0'),
                    original_index, 
                    self.delete_link, 
                    self.edit_link
                )
                self.link_layout.add_widget(card)
                Clock.schedule_once(lambda dt, c=card: self.update_card_height(c), 0.2)
            
            # 더 보기 버튼 (링크가 더 있을 경우)
            if end < len(links_to_display):
                more_btn = Button(
                    text='더 보기...',
                    size_hint_y=None,
                    height=dp(50),
                    background_color=hex_to_rgb(COLORS['primary_light']),
                    font_name=font_name
                )
                more_btn.bind(on_press=self.load_more)
                self.link_layout.add_widget(more_btn)
                self.link_layout.height += dp(50)
        
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 1), 0.1)
    
    def load_more(self, instance):
        """더 많은 링크 로드"""
        self.current_page += 1
        self.refresh_link_list()
    
    def update_card_height(self, card):
        """카드 높이를 링크 레이아웃에 반영"""
        self.link_layout.height += card.height
    
    def parse_search_query(self, query):
        tokens = []
        current_token = ""
        i = 0
        
        while i < len(query):
            if query[i:i+2].upper() in ['OR', 'AND']:
                if current_token:
                    tokens.append(current_token.strip())
                    current_token = ""
                tokens.append(query[i:i+2].upper())
                i += 2
            elif query[i:i+3].upper() == 'NOT':
                if current_token:
                    tokens.append(current_token.strip())
                    current_token = ""
                tokens.append('NOT')
                i += 3
            else:
                current_token += query[i]
                i += 1
        
        if current_token:
            tokens.append(current_token.strip())
        
        output = []
        stack = []
        precedence = {'OR': 1, 'AND': 2, 'NOT': 3}
        
        for token in tokens:
            if token.upper() in ['OR', 'AND', 'NOT']:
                while (stack and stack[-1] != '(' and 
                       precedence.get(stack[-1], 0) >= precedence.get(token, 0)):
                    output.append(stack.pop())
                stack.append(token.upper())
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                output.append(token)
        
        while stack:
            output.append(stack.pop())
        
        return output
    
    def evaluate_postfix(self, postfix_tokens):
        stack = []
        
        for token in postfix_tokens:
            if token == 'OR':
                if len(stack) < 2:
                    continue
                right = stack.pop()
                left = stack.pop()
                stack.append(lambda link: left(link) or right(link))
            elif token == 'AND':
                if len(stack) < 2:
                    continue
                right = stack.pop()
                left = stack.pop()
                stack.append(lambda link: left(link) and right(link))
            elif token == 'NOT':
                if len(stack) < 1:
                    continue
                operand = stack.pop()
                stack.append(lambda link: not operand(link))
            else:
                search_term = token.lower()
                def make_condition(term):
                    return lambda link: (
                        term in link['title'].lower() or
                        term in link['description'].lower() or
                        term in link['url'].lower()
                    )
                stack.append(make_condition(search_term))
        
        return stack[0] if stack else lambda link: False
    
    def search_links(self, instance):
        search_text = self.search_input.text.strip()
        self.current_page = 0  # 검색 시 첫 페이지부터
        
        try:
            if search_text:
                postfix_tokens = self.parse_search_query(search_text)
                condition_func = self.evaluate_postfix(postfix_tokens)
                self.displayed_links = [link for link in self.links if condition_func(link)]
            else:
                self.displayed_links = self.links.copy()
            
            self.search_mode = bool(search_text)
            self.sort_links(self.current_sort)
            
        except Exception as e:
            Logger.error(f'검색 중 오류: {e}')
            self.fallback_search(search_text)
    
    def fallback_search(self, search_text):
        search_text_lower = search_text.lower()
        self.displayed_links = []
        
        for link in self.links:
            if (search_text_lower in link['title'].lower() or 
                search_text_lower in link['description'].lower() or 
                search_text_lower in link['url'].lower()):
                self.displayed_links.append(link)
        
        self.search_mode = True
        self.sort_links(self.current_sort)
    
    def clear_search(self, instance):
        self.search_input.text = ''
        self.selected_category = 'all'
        self.category_btn.text = '전체포함'
        self.search_mode = False
        self.current_page = 0
        self.refresh_link_list()
    
    def sort_links(self, sort_type):
        self.current_sort = sort_type
        links_to_sort = self.displayed_links if self.search_mode else self.links
        self.current_page = 0  # 정렬 시 첫 페이지부터
        
        if sort_type == 'title_asc':
            links_to_sort.sort(key=lambda x: x['title'].lower())
        elif sort_type == 'title_desc':
            links_to_sort.sort(key=lambda x: x['title'].lower(), reverse=True)
        elif sort_type == 'url_asc':
            links_to_sort.sort(key=lambda x: x['url'].lower())
        elif sort_type == 'url_desc':
            links_to_sort.sort(key=lambda x: x['url'].lower(), reverse=True)
        
        self.refresh_link_list()
    
    def normalize_url(self, url):
        """URL을 정규화하고 소문자로 변환"""
        url = url.strip().lower()
        if url and not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        return url
    
    def check_duplicate_url(self, url):
        """URL 중복 체크 - 대소문자 구분 없이 비교"""
        normalized_url = self.normalize_url(url)
        duplicate_indices = []
        for i, link in enumerate(self.links):
            existing_url = self.normalize_url(link['url'])
            if existing_url == normalized_url:
                duplicate_indices.append(i)
        return duplicate_indices
    
    def count_duplicate_urls(self, url):
        """동일한 URL의 개수를 반환"""
        normalized_url = self.normalize_url(url)
        count = 0
        for link in self.links:
            existing_url = self.normalize_url(link['url'])
            if existing_url == normalized_url:
                count += 1
        return count
    
    def show_duplicate_popup(self, title, description, url, category, duplicate_indices):
        """중복 URL 처리 팝업"""
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        content.size_hint = (1, 1)
        
        font_name = get_font_name()
        
        current_duplicates = len(duplicate_indices)
        
        if current_duplicates >= 2:
            content.add_widget(Label(
                text=f'이미 같은 주소가 {current_duplicates}개 등록되어 있습니다.\n링크 주소 3개 이상 중복 등록 불가',
                color=hex_to_rgb(COLORS['white']),
                font_size=dp(16),
                size_hint_y=None,
                height=dp(80),
                font_name=font_name,
                text_size=(None, None),
                halign='center'
            ))
            
            button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
            
            ok_btn = Button(text='확인', background_color=hex_to_rgb(COLORS['primary']), font_name=font_name)
            
            def close_popup(btn):
                popup.dismiss()
            
            ok_btn.bind(on_press=close_popup)
            button_layout.add_widget(ok_btn)
            content.add_widget(button_layout)
            
            popup = Popup(
                title='',
                content=content,
                size_hint=(0.8, 0.5),
                auto_dismiss=False
            )
            popup.open()
            return
        
        content.add_widget(Label(
            text=f'이미 등록된 주소입니다:\n{self.links[duplicate_indices[0]]["title"]}',
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(16),
            size_hint_y=None,
            height=dp(80),
            font_name=font_name,
            text_size=(None, None),
            halign='center'
        ))
        
        button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        buttons = [
            ('기존항목 지우고 등록', hex_to_rgb(COLORS['primary'])),
            ('취소', hex_to_rgb(COLORS['accent'])),
            ('중복 등록', hex_to_rgb(COLORS['warning']))
        ]
        
        for text, color in buttons:
            btn = Button(text=text, background_color=color, font_name=font_name)
            button_layout.add_widget(btn)
        
        duplicate_btn, cancel_btn, replace_btn = button_layout.children
        
        def duplicate_link(btn):
            self.add_link(title, description, url, category)
            popup.dismiss()
        
        def cancel_add(btn):
            popup.dismiss()
        
        def replace_link(btn):
            for index in sorted(duplicate_indices, reverse=True):
                del self.links[index]
            self.add_link(title, description, url, category)
            popup.dismiss()
        
        duplicate_btn.bind(on_press=duplicate_link)
        cancel_btn.bind(on_press=cancel_add)
        replace_btn.bind(on_press=replace_link)
        
        content.add_widget(button_layout)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False
        )
        
        popup.open()
    
    def show_add_link_popup(self, instance):
        font_name = get_font_name()
        
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        self.title_input = TextInput(
            hint_text='사이트 제목을 입력하세요',
            size_hint_y=None,
            height=dp(50),
            font_name=font_name
        )
        
        self.desc_input = TextInput(
            hint_text='사이트 설명을 입력하세요\n(여러 줄로 입력 가능)',
            size_hint_y=None,
            height=dp(100),
            multiline=True,
            font_name=font_name
        )
        
        self.url_input = TextInput(
            hint_text='https://example.com',
            size_hint_y=None,
            height=dp(50),
            font_name=font_name
        )
        
        button_category_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        cancel_btn = Button(
            text='취소', 
            background_color=hex_to_rgb(COLORS['accent']),
            size_hint=(0.3, 1),
            font_name=font_name
        )
        
        self.category_select_btn = Button(
            text='0. 분류안함',
            size_hint=(0.4, 1),
            background_color=hex_to_rgb(COLORS['primary_light']),
            font_name=font_name
        )
        self.category_select_btn.bind(on_press=self.show_add_category_popup)
        
        save_btn = Button(
            text='저장', 
            background_color=hex_to_rgb(COLORS['primary']),
            size_hint=(0.3, 1),
            font_name=font_name
        )
        
        button_category_layout.add_widget(cancel_btn)
        button_category_layout.add_widget(self.category_select_btn)
        button_category_layout.add_widget(save_btn)
        
        self.selected_category_id = '0'
        
        def save_link(btn):
            title = self.title_input.text.strip()
            description = self.desc_input.text.strip()
            url = self.url_input.text.strip()
            
            if title and url:
                normalized_url = self.normalize_url(url)
                duplicate_indices = self.check_duplicate_url(normalized_url)
                if duplicate_indices:
                    popup.dismiss()
                    self.show_duplicate_popup(title, description, normalized_url, self.selected_category_id, duplicate_indices)
                else:
                    self.add_link(title, description, normalized_url, self.selected_category_id)
                    popup.dismiss()
        
        def close_popup(btn):
            popup.dismiss()
        
        save_btn.bind(on_press=save_link)
        cancel_btn.bind(on_press=close_popup)
        
        content.add_widget(Label(
            text='새 링크 추가', 
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            font_name=font_name
        ))
        content.add_widget(self.title_input)
        content.add_widget(self.desc_input)
        content.add_widget(self.url_input)
        content.add_widget(button_category_layout)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.85, 0.8),
            auto_dismiss=False
        )
        
        popup.open()
        Clock.schedule_once(lambda dt: setattr(self.title_input, 'focus', True), 0.1)
    
    def show_add_category_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        font_name = get_font_name()
        
        content.add_widget(Label(
            text='분류 선택',
            color=hex_to_rgb(COLORS['text_primary']),
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            font_name=font_name
        ))
        
        scroll = ScrollView(do_scroll_x=False)
        category_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        category_layout.bind(minimum_height=category_layout.setter('height'))
        
        for cat_id, cat_name in CATEGORIES.items():
            btn = CategoryToggleButton(text=f'{cat_id}. {cat_name}')
            btn.bind(on_press=lambda x, cid=cat_id: self.select_add_category(cid, popup))
            if self.selected_category_id == cat_id:
                btn.state = 'down'
            category_layout.add_widget(btn)
        
        category_layout.height = len(CATEGORIES) * dp(35)
        scroll.add_widget(category_layout)
        content.add_widget(scroll)
        
        close_btn = Button(
            text='닫기',
            size_hint_y=None,
            height=dp(40),
            background_color=hex_to_rgb(COLORS['accent']),
            font_name=font_name
        )
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.7, 0.7),
            auto_dismiss=False
        )
        popup.open()
    
    def select_add_category(self, category_id, popup):
        self.selected_category_id = category_id
        self.category_select_btn.text = f'{category_id}. {CATEGORIES[category_id]}'
        popup.dismiss()
    
    def edit_link(self, index):
        if index < 0 or index >= len(self.links):
            return
        
        link = self.links[index]
        font_name = get_font_name()
        
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        title_input = TextInput(
            text=link['title'],
            size_hint_y=None,
            height=dp(50),
            font_name=font_name
        )
        
        desc_input = TextInput(
            text=link['description'],
            size_hint_y=None,
            height=dp(100),
            multiline=True,
            font_name=font_name
        )
        
        url_input = TextInput(
            text=link['url'],
            size_hint_y=None,
            height=dp(50),
            font_name=font_name
        )
        
        button_category_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        cancel_btn = Button(
            text='취소', 
            background_color=hex_to_rgb(COLORS['accent']),
            size_hint=(0.3, 1),
            font_name=font_name
        )
        
        current_category = link.get('category', '0')
        category_select_btn = Button(
            text=f'{current_category}. {CATEGORIES.get(current_category, "분류안함")}',
            size_hint=(0.4, 1),
            background_color=hex_to_rgb(COLORS['primary_light']),
            font_name=font_name
        )
        
        save_btn = Button(
            text='수정', 
            background_color=hex_to_rgb(COLORS['primary']),
            size_hint=(0.3, 1),
            font_name=font_name
        )
        
        button_category_layout.add_widget(cancel_btn)
        button_category_layout.add_widget(category_select_btn)
        button_category_layout.add_widget(save_btn)
        
        edit_selected_category = current_category
        
        def show_edit_category_popup(instance):
            edit_content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
            
            edit_content.add_widget(Label(
                text='분류 선택',
                color=hex_to_rgb(COLORS['text_primary']),
                font_size=dp(18),
                bold=True,
                size_hint_y=None,
                height=dp(40),
                font_name=font_name
            ))
            
            scroll = ScrollView(do_scroll_x=False)
            edit_category_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
            edit_category_layout.bind(minimum_height=edit_category_layout.setter('height'))
            
            for cat_id, cat_name in CATEGORIES.items():
                btn = CategoryToggleButton(text=f'{cat_id}. {cat_name}')
                btn.bind(on_press=lambda x, cid=cat_id: select_edit_category(cid, edit_popup))
                if edit_selected_category == cat_id:
                    btn.state = 'down'
                edit_category_layout.add_widget(btn)
            
            edit_category_layout.height = len(CATEGORIES) * dp(35)
            scroll.add_widget(edit_category_layout)
            edit_content.add_widget(scroll)
            
            close_btn = Button(
                text='닫기',
                size_hint_y=None,
                height=dp(40),
                background_color=hex_to_rgb(COLORS['accent']),
                font_name=font_name
            )
            close_btn.bind(on_press=lambda x: edit_popup.dismiss())
            edit_content.add_widget(close_btn)
            
            edit_popup = Popup(
                title='',
                content=edit_content,
                size_hint=(0.7, 0.7),
                auto_dismiss=False
            )
            edit_popup.open()
        
        def select_edit_category(category_id, popup):
            nonlocal edit_selected_category
            edit_selected_category = category_id
            category_select_btn.text = f'{category_id}. {CATEGORIES[category_id]}'
            popup.dismiss()
        
        category_select_btn.bind(on_press=show_edit_category_popup)
        
        def save_edit(btn):
            new_title = title_input.text.strip()
            new_description = desc_input.text.strip()
            new_url = url_input.text.strip()
            
            if new_title and new_url:
                normalized_url = self.normalize_url(new_url)
                
                duplicate_indices = []
                for i, existing_link in enumerate(self.links):
                    if i != index:
                        existing_url = self.normalize_url(existing_link['url'])
                        if existing_url == normalized_url:
                            duplicate_indices.append(i)
                
                if duplicate_indices:
                    popup.dismiss()
                    self.show_edit_duplicate_popup(new_title, new_description, normalized_url, edit_selected_category, index, duplicate_indices)
                else:
                    self.update_link(index, new_title, new_description, normalized_url, edit_selected_category)
                    popup.dismiss()
        
        def cancel_edit(btn):
            popup.dismiss()
        
        save_btn.bind(on_press=save_edit)
        cancel_btn.bind(on_press=cancel_edit)
        
        content.add_widget(Label(
            text='링크 수정', 
            color=hex_to_rgb(COLORS['text_primary']),
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            font_name=font_name
        ))
        content.add_widget(title_input)
        content.add_widget(desc_input)
        content.add_widget(url_input)
        content.add_widget(button_category_layout)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.85, 0.8),
            auto_dismiss=False
        )
        
        popup.open()
        Clock.schedule_once(lambda dt: setattr(title_input, 'focus', True), 0.1)
    
    def show_edit_duplicate_popup(self, title, description, url, category, edit_index, duplicate_indices):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        font_name = get_font_name()
        
        current_duplicates = len(duplicate_indices)
        
        if current_duplicates >= 2:
            content.add_widget(Label(
                text=f'이미 같은 주소가 {current_duplicates}개 등록되어 있습니다.\n링크 주소 3개 이상 중복 등록 불가',
                color=hex_to_rgb(COLORS['white']),
                font_size=dp(16),
                size_hint_y=None,
                height=dp(80),
                font_name=font_name,
                text_size=(None, None),
                halign='center'
            ))
            
            button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
            
            ok_btn = Button(text='확인', background_color=hex_to_rgb(COLORS['primary']), font_name=font_name)
            
            def close_popup(btn):
                popup.dismiss()
            
            ok_btn.bind(on_press=close_popup)
            button_layout.add_widget(ok_btn)
            content.add_widget(button_layout)
            
            popup = Popup(
                title='',
                content=content,
                size_hint=(0.8, 0.5),
                auto_dismiss=False
            )
            popup.open()
            return
        
        content.add_widget(Label(
            text=f'다른 항목에 같은 주소가 있습니다:\n{self.links[duplicate_indices[0]]["title"]}',
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(16),
            size_hint_y=None,
            height=dp(80),
            font_name=font_name,
            text_size=(None, None),
            halign='center'
        ))
        
        button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        
        buttons = [
            ('기존항목 유지', hex_to_rgb(COLORS['primary'])),
            ('취소', hex_to_rgb(COLORS['accent'])),
            ('기존항목 지우고 수정', hex_to_rgb(COLORS['warning']))
        ]
        
        for text, color in buttons:
            btn = Button(text=text, background_color=color, font_name=font_name)
            button_layout.add_widget(btn)
        
        keep_btn, cancel_btn, replace_btn = button_layout.children
        
        def keep_original(btn):
            self.update_link(edit_index, title, description, url, category)
            popup.dismiss()
        
        def cancel_edit(btn):
            popup.dismiss()
        
        def replace_and_edit(btn):
            for index in sorted(duplicate_indices, reverse=True):
                del self.links[index]
            adjusted_index = edit_index
            for dup_index in duplicate_indices:
                if dup_index < edit_index:
                    adjusted_index -= 1
            self.update_link(adjusted_index, title, description, url, category)
            popup.dismiss()
        
        keep_btn.bind(on_press=keep_original)
        cancel_btn.bind(on_press=cancel_edit)
        replace_btn.bind(on_press=replace_and_edit)
        
        content.add_widget(button_layout)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.5),
            auto_dismiss=False
        )
        
        popup.open()
    
    def update_link(self, index, title, description, url, category):
        if 0 <= index < len(self.links):
            self.links[index] = {
                'title': title,
                'description': description,
                'url': url,
                'category': category
            }
            self.save_links()
            self.refresh_link_list()
    
    def delete_link(self, index):
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        font_name = get_font_name()
        
        content.add_widget(Label(
            text=f'"{self.links[index]["title"]}" 링크를 삭제하시겠습니까?',
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(16),
            size_hint_y=None,
            height=dp(60),
            font_name=font_name,
            text_size=(None, None),
            halign='center'
        ))
        
        button_layout = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        cancel_btn = Button(text='취소', background_color=hex_to_rgb(COLORS['accent']), font_name=font_name)
        delete_btn = Button(text='삭제', background_color=hex_to_rgb(COLORS['danger']), font_name=font_name)
        
        def confirm_delete(btn):
            if 0 <= index < len(self.links):
                del self.links[index]
                self.save_links()
                self.refresh_link_list()
            popup.dismiss()
        
        def cancel_delete(btn):
            popup.dismiss()
        
        delete_btn.bind(on_press=confirm_delete)
        cancel_btn.bind(on_press=cancel_delete)
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(delete_btn)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.7, 0.4),
            auto_dismiss=False
        )
        
        popup.open()
    
    def add_link(self, title, description, url, category):
        new_link = {
            'title': title,
            'description': description,
            'url': url,
            'category': category
        }
        self.links.append(new_link)
        self.save_links()
        self.refresh_link_list()
    
    def save_links(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.links, f, ensure_ascii=False, indent=2)
        except Exception as e:
            Logger.error(f'링크 저장 실패: {e}')
    
    def confirm_exit(self):
        """뒤로가기 두 번 누르면 종료"""
        if self._exit_pressed:
            App.get_running_app().stop()
        else:
            self._exit_pressed = True
            self.show_toast('한 번 더 누르면 종료됩니다')
            Clock.schedule_once(lambda dt: setattr(self, '_exit_pressed', False), 2)
    
    def show_toast(self, message):
        """간단한 토스트 메시지"""
        content = BoxLayout(orientation='vertical', padding=dp(20))
        content.add_widget(Label(
            text=message,
            color=hex_to_rgb(COLORS['white']),
            font_size=dp(16),
            font_name=get_font_name()
        ))
        
        popup = Popup(
            content=content,
            size_hint=(0.5, 0.2),
            background_color=hex_to_rgb(COLORS['primary_dark']),
            auto_dismiss=True
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)

# ============================================================
# 앱 실행
# ============================================================

class SannaeeumLinkApp(App):
    def build(self):
        Window.clearcolor = hex_to_rgb(COLORS['background'])
        self.title = '산내음 링크'
        self.icon = 'icon.png'
        
        # 뒤로가기 버튼 바인딩
        Window.bind(on_keyboard=self.on_keyboard)
        
        return LinkApp()
    
    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if key == 27:  # 뒤로가기 버튼
            if hasattr(self.root, 'confirm_exit'):
                self.root.confirm_exit()
            return True
        return False

if __name__ == '__main__':
    print("산내음 링크 앱 시작 중...")
    print(f"마루부리 폰트 사용 가능: {KOREAN_FONT_AVAILABLE}")
    print(f"데이터 저장 경로: {DATA_DIR}")
    try:
        SannaeeumLinkApp().run()
    except Exception as e:
        print(f"앱 실행 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        if not IS_ANDROID:
            input("엔터 키를 누르면 종료됩니다...")
