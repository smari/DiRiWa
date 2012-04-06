from django.contrib import admin
from diriwa import models

#class CommentInline(admin.TabularInline):
#   model = models.Comment
#   max_num = 1
#
#class ThingyAdmin(admin.ModelAdmin):
#   list_display = ('field1', 'field2', 'field3')
#   list_filter = ('field1', 'field2', 'field3')
#   inlines = [CommentInline, ]
#admin.site.register(models.Thingy, ThingyAdmin)

class LanguageAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Language, LanguageAdmin)

class TripleAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Triple, TripleAdmin)

class EntityAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Entity, EntityAdmin)

class RegionTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.RegionType, RegionTypeAdmin)

class RegionAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Region, RegionAdmin)

class RegionLocalNameAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.RegionLocalName, RegionLocalNameAdmin)

class RegionMembershipAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.RegionMembership, RegionMembershipAdmin)

class TopicAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Topic, TopicAdmin)

class SectionHistoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.SectionHistory, SectionHistoryAdmin)

class SectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Section, SectionAdmin)

class SectionVoteAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.SectionVote, SectionVoteAdmin)

class TagAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Tag, TagAdmin)

class EntityTagAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.EntityTag, EntityTagAdmin)

class CourtCaseAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.CourtCase, CourtCaseAdmin)

class NewsItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.NewsItem, NewsItemAdmin)

class LinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Link, LinkAdmin)
