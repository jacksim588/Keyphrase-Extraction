INSERT INTO public.phrases_in_xml(xml_id,phrase_id)
SELECT public.brandbankxml_test.xml_id, public."Phrases".phrase_id
FROM public.brandbankxml_test
JOIN public."Phrases"
ON public.brandbankxml_test.text LIKE '%' || public."Phrases".phrase || '%';