"""
    End User를 위한 간단한 api


"""

from .saint import Saint
import copy


def get(course_type, year_range, semesters, **kwargs):
    """
    THIS IS THE END POINT OF pysaint API
    USAGE::

        >>> import pysaint
        >>> res = pysaint.get('전공', ['2018'], ['2 학기'])
        >>> print(res)


        >>> res = pysaint.get('교양필수', range(2015, 2017), ['1 학기', '여름학기', '2 학기', '겨울학기'])
        >>> print(res)


        >>> res = pysaint.get('교양선택', (2016, 2017, 2018), ('1 학기', ))
        >>> print(res)


    :param course_type:
    :type course_type: str
    example )
            '교양필수'
            '전공'
            '교양선택'
    :param year_range:
    :type year_range: list or tuple
    :param semesters:
    :type semesters: list or tuple
    :return: dict
    """
    if course_type == '교양필수':
        return _liberal_arts(year_range=year_range, semesters=semesters, **kwargs)
    elif course_type == '전공':
        return _major(year_range=year_range, semesters=semesters, **kwargs)
    elif course_type == '교양선택':
        return _selective_liberal(year_range=year_range, semesters=semesters, **kwargs)
    else:
        raise Exception("Unexpected param course_type {} \n".format(
            course_type
        ))


def _liberal_arts(year_range=[], semesters=[], **kwargs):
    """
    TODO: validate parameters!
    교양필수 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :type year_range: list or tuple
    example input )
            [2013, 2014, 2015, 2016, 2017, 2018]
            or
            (2017, 2018)
    :param semesters:
    :type semesters: list or tuple
    example input )
            ['1 학기', '여름학기', '2 학기', '겨울학기']
            or
            ('1 학기')
    :return:
    {
        2013: {
            '전체학년': {
                'CHAPEL': [
                    {
                        dictionary which has
                        dict_keys(['계획', '이수구분(주전공)',
                        '이수구분(다전공)', '공학인증', '교과영역',
                        '과목번호', '과목명', '분반', '교수명',
                        '개설학과', '시간/학점(설계)', '수강인원',
                        '여석', '강의시간(강의실)', '수강대상'])
                    }
                ],
                '컴퓨터활용1(Excel)': [],
                '컴퓨터활용2(PPT)': [],
                'Practical Reading ＆ Writing': [],
                '현대인과성서2': []
                }
            }
            '1학년': {...},
            '2학년': {...},
            '3학년': {...},
            '4학년': {...},
            '5학년': {...}
        },
        year: {
            grade: {
                course_name: [] <- list which has dictionaries as it's elements
            }
        }
    }
    """
    ret = {year: {} for year in year_range}
    saint = Saint()
    saint.select_course_section('교양필수')

    def __get_whole_course(year, semester):
        print('{} {}'.format(year, semester))
        saint.select_year(year)
        saint.select_semester(semester)
        liberal_map = saint.get_liberal_arts_map()
        course_map = copy.deepcopy(liberal_map)

        for grade in liberal_map:
            course_map[grade] = {course_name: {} for course_name in liberal_map[grade]}

        for grade in liberal_map:
            for course_name in liberal_map[grade]:
                if course_name != '':
                    course_map[grade][course_name] = saint.select_on_liberal_arts(grade, course_name)

        return course_map

    for year in year_range:
        for semester in semesters:
            course_bunch = __get_whole_course(year, semester)
            ret[year][semester] = course_bunch

    return ret


def _major(year_range=[], semesters=[], **kwargs):
    """
    전공 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :type year_range: list or tuple
    :param semesters:
    :type semesters: list or tuple
    :return:
    {
        '2017': {
            '1 학기': {
                '인문대학': {
                    '중어중문학과': {
                        '중어중문학과': [
                            {
                                '계획': '\xa0',
                                '이수구분(주전공)': '전선-중문',
                                '이수구분(다전공)': '복선-중문/부선-중문',
                                '공학인증': '\xa0',
                                '교과영역': '7+1교과목\n인턴쉽(장기과정)\n인턴쉽',
                                '과목번호': '5010611601',
                                '과목명': '국내장기현장실습(3)',
                                '분반': '\xa0',
                                '교수명': '\xa0',
                                '개설학과': '경력개발팀',
                                '시간/학점(설계)': '3.00 /3',
                                '수강인원': '1',
                                '여석': '199',
                                '강의시간(강의실)': '\xa0',
                                '수강대상': '전체'
                            },
                            {
                                ...
                                dict_keys(['계획', '이수구분(주전공)', '이수구분(다전공)', '공학인증', '교과영역',
                                '과목번호', '과목명', '분반', '교수명', '개설학과', '시간/학점(설계)', '수강인원',
                                '여석', '강의시간(강의실)', '수강대상'])
                            }
                        ]
                    },
                    '국어국문학과': {},
                    '일어일문학과': {},
                    '영어영문학과': {},
                    '불어불문학과': {},
                    '철학과': {},
                    '사학과': {},
                    '기독교학과': {},
                },
                '자연과학대학': {},
                '법과대학': {},
                '사회과학대학': {},
                '경제통상대학': {},
                '경영대학': {},
                '공과대학': {},
                'IT대학': {},
                '베어드학부대학': {},
                '예술창작학부': {},
                '스포츠학부': {},
                '융합특성화자유전공학부': {}
            }
        },
        'year': {
            'semester': {
                'college': {
                    'faculty': {
                        'major': [
                            {
                                dict_keys(['계획', '이수구분(주전공)', '이수구분(다전공)', '공학인증', '교과영역',
                                '과목번호', '과목명', '분반', '교수명', '개설학과', '시간/학점(설계)', '수강인원',
                                '여석', '강의시간(강의실)', '수강대상'])
                            }
                        ]
                    }
                }
            }
        }
    }
    """

    ret = {year: {} for year in year_range}
    saint = Saint()

    def __get_whole_course(year, semester):
        print('{} {}'.format(year, semester))
        saint.select_year(year)
        saint.select_semester(semester)
        major_map = saint.get_major_map()
        course_map = copy.deepcopy(major_map)

        for college in major_map:
            for faculty in major_map[college]:
                course_map[college][faculty] = {key: [] for key in major_map[college][faculty]}

        for college in major_map:
            for faculty in major_map[college]:
                for major in major_map[college][faculty]:
                    print('{} {} {}'.format(college, faculty, major))
                    course_map[college][faculty][major] = saint.select_on_major(college, faculty, major)

        return course_map

    for year in year_range:
        for semester in semesters:
            course_bunch = __get_whole_course(year, semester)
            ret[year][semester] = course_bunch

    return ret


def _selective_liberal(year_range=[], semesters=[], **kwargs):
    """
    교양선택 과목들을 학기 단위로 묶어서 반환한다.
    :param year_range:
    :param semesters:
    :return:
    """
    ret = {year: {} for year in year_range}
    saint = Saint()
    saint.select_course_section('교양선택')

    # is this necessary job?
    saint.select_year('2017')
    saint.select_semester('2 학기')

    def __get_whole_course(year, semester):
        print('{} {}'.format(year, semester))
        saint.select_year(year)
        saint.select_semester(semester)
        selective_map = saint.get_selective_liberal_map()
        course_map = {course_name: {} for course_name in selective_map}

        for course_name in selective_map:
            if course_name != '':
                course_map[course_name] = saint.select_on_selective_liberal(course_name)

        return course_map

    for year in year_range:
        for semester in semesters:
            course_bunch = __get_whole_course(year, semester)
            ret[year][semester] = course_bunch

    return ret


def cyber(year_range=[], semesters=[], **kwargs):
    """
    TODO:
    시간나면 만들기
    :param year_range:
    :param semesters:
    :return:
    """
